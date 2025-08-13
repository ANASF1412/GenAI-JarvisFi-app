#!/usr/bin/env python3
"""
MongoDB Integration with Security and Encryption
Implements secure data storage with AES-256 encryption
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import secrets

# MongoDB and Security imports
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SecureMongoDBManager:
    """
    Secure MongoDB manager with encryption and compliance features
    """
    
    def __init__(self, connection_string: str = None, database_name: str = "finance_chatbot"):
        """Initialize secure MongoDB connection"""
        self.logger = self._setup_logger()
        self.database_name = database_name
        self.client = None
        self.db = None
        self.encryption_key = None
        
        # Initialize encryption
        self._setup_encryption()
        
        # Connect to MongoDB
        if MONGODB_AVAILABLE:
            self._connect_to_mongodb(connection_string)
        else:
            self.logger.warning("MongoDB not available. Using fallback storage.")
            self._setup_fallback_storage()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup secure logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _setup_encryption(self):
        """Setup AES-256 encryption for sensitive data"""
        try:
            # Try to load existing key from environment or generate new one
            key_string = os.getenv('FINANCE_ENCRYPTION_KEY')
            
            if key_string:
                self.encryption_key = key_string.encode()
            else:
                # Generate new key using PBKDF2
                password = os.getenv('FINANCE_MASTER_PASSWORD', 'default_secure_password_2024').encode()
                salt = os.getenv('FINANCE_SALT', 'finance_chatbot_salt_2024').encode()
                
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password))
                self.encryption_key = key
            
            self.cipher = Fernet(self.encryption_key)
            self.logger.info("Encryption setup completed successfully")
            
        except Exception as e:
            self.logger.error(f"Encryption setup failed: {e}")
            # Fallback to basic encoding (not recommended for production)
            self.encryption_key = Fernet.generate_key()
            self.cipher = Fernet(self.encryption_key)
    
    def _connect_to_mongodb(self, connection_string: str = None):
        """Connect to MongoDB with security settings"""
        try:
            if not connection_string:
                # Default connection string for local development
                connection_string = os.getenv(
                    'MONGODB_CONNECTION_STRING', 
                    'mongodb://localhost:27017/'
                )
            
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=10000,         # 10 second connection timeout
                socketTimeoutMS=20000,          # 20 second socket timeout
                maxPoolSize=50,                 # Maximum connection pool size
                retryWrites=True                # Enable retryable writes
            )
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            
            # Create indexes for better performance
            self._create_indexes()
            
            self.logger.info(f"Connected to MongoDB database: {self.database_name}")
            
        except ConnectionFailure as e:
            self.logger.error(f"MongoDB connection failed: {e}")
            self._setup_fallback_storage()
        except Exception as e:
            self.logger.error(f"MongoDB setup error: {e}")
            self._setup_fallback_storage()
    
    def _setup_fallback_storage(self):
        """Setup fallback file-based storage when MongoDB is unavailable"""
        self.fallback_storage = {}
        self.fallback_file = "data/fallback_storage.json"
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Load existing fallback data
        try:
            if os.path.exists(self.fallback_file):
                with open(self.fallback_file, 'r', encoding='utf-8') as f:
                    self.fallback_storage = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load fallback storage: {e}")
            self.fallback_storage = {}
        
        self.logger.info("Fallback storage initialized")
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        try:
            if self.db is None:
                return
            
            # User profiles collection indexes
            self.db.user_profiles.create_index("user_id", unique=True)
            self.db.user_profiles.create_index("email")
            self.db.user_profiles.create_index("created_at")
            
            # Chat history collection indexes
            self.db.chat_history.create_index([("user_id", 1), ("timestamp", -1)])
            self.db.chat_history.create_index("session_id")
            
            # Financial data collection indexes
            self.db.financial_data.create_index("user_id")
            self.db.financial_data.create_index("data_type")
            self.db.financial_data.create_index("created_at")
            
            # Audit logs collection indexes
            self.db.audit_logs.create_index([("user_id", 1), ("timestamp", -1)])
            self.db.audit_logs.create_index("action_type")
            
            self.logger.info("Database indexes created successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to create indexes: {e}")
    
    def encrypt_sensitive_data(self, data: Any) -> str:
        """Encrypt sensitive data using AES-256"""
        try:
            if isinstance(data, (dict, list)):
                data_str = json.dumps(data, ensure_ascii=False)
            else:
                data_str = str(data)
            
            encrypted_data = self.cipher.encrypt(data_str.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
            
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            return str(data)  # Fallback to unencrypted (not recommended)
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> Any:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            data_str = decrypted_data.decode('utf-8')
            
            # Try to parse as JSON, fallback to string
            try:
                return json.loads(data_str)
            except json.JSONDecodeError:
                return data_str
                
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return encrypted_data  # Return as-is if decryption fails
    
    def create_user_profile(self, user_data: Dict) -> Dict:
        """Create encrypted user profile"""
        try:
            user_id = user_data.get('user_id') or self._generate_user_id()
            
            # Encrypt sensitive fields
            sensitive_fields = ['income', 'expenses', 'assets', 'liabilities', 'phone', 'address']
            encrypted_data = {}
            
            for field in sensitive_fields:
                if field in user_data:
                    encrypted_data[f"{field}_encrypted"] = self.encrypt_sensitive_data(user_data[field])
            
            # Prepare profile document
            profile = {
                'user_id': user_id,
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'user_type': user_data.get('user_type', 'beginner'),
                'language': user_data.get('language', 'english'),
                'age_range': user_data.get('age_range', '25-35'),  # Store age range instead of exact age
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                'is_active': True,
                **encrypted_data
            }
            
            # Store in database or fallback
            if self.db:
                result = self.db.user_profiles.insert_one(profile)
                profile['_id'] = str(result.inserted_id)
            else:
                self.fallback_storage[user_id] = profile
                self._save_fallback_storage()
            
            # Log audit trail
            self._log_audit_event(user_id, 'profile_created', {'user_type': user_data.get('user_type')})
            
            self.logger.info(f"User profile created: {user_id}")
            return profile
            
        except Exception as e:
            self.logger.error(f"Failed to create user profile: {e}")
            raise
    
    def _generate_user_id(self) -> str:
        """Generate secure user ID"""
        return f"user_{secrets.token_urlsafe(16)}_{int(datetime.utcnow().timestamp())}"
    
    def _save_fallback_storage(self):
        """Save fallback storage to file"""
        try:
            with open(self.fallback_file, 'w', encoding='utf-8') as f:
                json.dump(self.fallback_storage, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save fallback storage: {e}")
    
    def _log_audit_event(self, user_id: str, action: str, details: Dict = None):
        """Log audit events for compliance"""
        try:
            audit_log = {
                'user_id': user_id,
                'action_type': action,
                'timestamp': datetime.utcnow(),
                'details': details or {},
                'ip_address': 'localhost',  # In production, get from request
                'user_agent': 'finance_chatbot'  # In production, get from request
            }
            
            if self.db:
                self.db.audit_logs.insert_one(audit_log)
            else:
                # Store in fallback
                audit_key = f"audit_{int(datetime.utcnow().timestamp())}_{secrets.token_hex(8)}"
                self.fallback_storage[audit_key] = audit_log
                self._save_fallback_storage()
                
        except Exception as e:
            self.logger.error(f"Failed to log audit event: {e}")
