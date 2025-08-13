#!/usr/bin/env python3
"""
Security Manager for Personal Finance Chatbot
Implements OAuth 2.0, JWT validation, and security compliance
"""

import os
import jwt
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json
import re

# Firebase Auth (optional)
try:
    import firebase_admin
    from firebase_admin import credentials, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

# Additional security libraries
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

class SecurityManager:
    """
    Comprehensive security manager for the finance chatbot
    """
    
    def __init__(self):
        """Initialize security manager"""
        self.logger = self._setup_logger()
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', self._generate_jwt_secret())
        self.jwt_algorithm = 'HS256'
        self.token_expiry_hours = 24
        
        # Initialize Firebase if available
        self._setup_firebase()
        
        # Security policies
        self.password_policy = {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_numbers': True,
            'require_special': True
        }
        
        # Rate limiting
        self.rate_limits = {
            'login_attempts': {'max': 5, 'window': 900},  # 5 attempts per 15 minutes
            'api_calls': {'max': 1000, 'window': 3600},   # 1000 calls per hour
            'chat_messages': {'max': 100, 'window': 3600} # 100 messages per hour
        }
        
        self.failed_attempts = {}
        self.api_call_counts = {}
        
        self.logger.info("Security manager initialized")
    
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
    
    def _generate_jwt_secret(self) -> str:
        """Generate secure JWT secret"""
        return secrets.token_urlsafe(64)
    
    def _setup_firebase(self):
        """Setup Firebase authentication if available"""
        try:
            if FIREBASE_AVAILABLE:
                # Initialize Firebase (in production, use service account key)
                firebase_config = os.getenv('FIREBASE_CONFIG')
                if firebase_config and not firebase_admin._apps:
                    cred = credentials.Certificate(json.loads(firebase_config))
                    firebase_admin.initialize_app(cred)
                    self.logger.info("Firebase authentication initialized")
                else:
                    self.logger.info("Firebase config not found, using local auth")
            else:
                self.logger.info("Firebase not available, using local authentication")
        except Exception as e:
            self.logger.error(f"Firebase setup failed: {e}")
    
    def validate_password(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password against security policy"""
        errors = []
        
        if len(password) < self.password_policy['min_length']:
            errors.append(f"Password must be at least {self.password_policy['min_length']} characters long")
        
        if self.password_policy['require_uppercase'] and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.password_policy['require_lowercase'] and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.password_policy['require_numbers'] and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if self.password_policy['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def hash_password(self, password: str) -> str:
        """Hash password securely"""
        try:
            if BCRYPT_AVAILABLE:
                # Use bcrypt for secure hashing
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
                return hashed.decode('utf-8')
            else:
                # Fallback to PBKDF2 (less secure but available)
                salt = secrets.token_hex(32)
                hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
                return f"{salt}:{hashed.hex()}"
        except Exception as e:
            self.logger.error(f"Password hashing failed: {e}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            if BCRYPT_AVAILABLE and not ':' in hashed_password:
                # bcrypt format
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            else:
                # PBKDF2 format
                salt, stored_hash = hashed_password.split(':')
                computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
                return computed_hash.hex() == stored_hash
        except Exception as e:
            self.logger.error(f"Password verification failed: {e}")
            return False
    
    def generate_jwt_token(self, user_data: Dict) -> str:
        """Generate JWT token for authenticated user"""
        try:
            payload = {
                'user_id': user_data.get('user_id'),
                'email': user_data.get('email'),
                'user_type': user_data.get('user_type', 'beginner'),
                'language': user_data.get('language', 'english'),
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
                'iss': 'finance_chatbot',
                'aud': 'finance_chatbot_users'
            }
            
            token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            self.logger.info(f"JWT token generated for user: {user_data.get('user_id')}")
            return token
            
        except Exception as e:
            self.logger.error(f"JWT token generation failed: {e}")
            raise
    
    def validate_jwt_token(self, token: str) -> Tuple[bool, Dict]:
        """Validate JWT token"""
        try:
            payload = jwt.decode(
                token, 
                self.jwt_secret, 
                algorithms=[self.jwt_algorithm],
                audience='finance_chatbot_users',
                issuer='finance_chatbot'
            )
            
            # Check if token is expired
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return False, {'error': 'Token expired'}
            
            return True, payload
            
        except jwt.ExpiredSignatureError:
            return False, {'error': 'Token expired'}
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid token: {e}")
            return False, {'error': 'Invalid token'}
        except Exception as e:
            self.logger.error(f"Token validation failed: {e}")
            return False, {'error': 'Token validation failed'}
    
    def check_rate_limit(self, user_id: str, action_type: str) -> Tuple[bool, Dict]:
        """Check if user has exceeded rate limits"""
        try:
            current_time = datetime.utcnow()
            
            if action_type not in self.rate_limits:
                return True, {}
            
            limit_config = self.rate_limits[action_type]
            window_start = current_time - timedelta(seconds=limit_config['window'])
            
            # Initialize tracking for user if not exists
            if user_id not in self.api_call_counts:
                self.api_call_counts[user_id] = {}
            
            if action_type not in self.api_call_counts[user_id]:
                self.api_call_counts[user_id][action_type] = []
            
            # Clean old entries
            self.api_call_counts[user_id][action_type] = [
                timestamp for timestamp in self.api_call_counts[user_id][action_type]
                if timestamp > window_start
            ]
            
            # Check if limit exceeded
            current_count = len(self.api_call_counts[user_id][action_type])
            
            if current_count >= limit_config['max']:
                return False, {
                    'error': 'Rate limit exceeded',
                    'limit': limit_config['max'],
                    'window': limit_config['window'],
                    'current_count': current_count,
                    'reset_time': window_start + timedelta(seconds=limit_config['window'])
                }
            
            # Record this request
            self.api_call_counts[user_id][action_type].append(current_time)
            
            return True, {
                'remaining': limit_config['max'] - current_count - 1,
                'reset_time': window_start + timedelta(seconds=limit_config['window'])
            }
            
        except Exception as e:
            self.logger.error(f"Rate limit check failed: {e}")
            return True, {}  # Allow request if check fails
    
    def sanitize_input(self, user_input: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        try:
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\']', '', user_input)
            
            # Limit length
            sanitized = sanitized[:1000]
            
            # Remove SQL injection patterns
            sql_patterns = [
                r'(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)',
                r'(--|#|/\*|\*/)',
                r'(\bOR\b.*=.*\bOR\b)',
                r'(\bAND\b.*=.*\bAND\b)'
            ]
            
            for pattern in sql_patterns:
                sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
            
            return sanitized.strip()
            
        except Exception as e:
            self.logger.error(f"Input sanitization failed: {e}")
            return ""
    
    def validate_financial_data(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validate financial data for security and compliance"""
        errors = []
        
        try:
            # Check for required fields
            required_fields = ['user_id', 'data_type']
            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")
            
            # Validate numeric fields
            numeric_fields = ['income', 'expenses', 'assets', 'liabilities', 'amount']
            for field in numeric_fields:
                if field in data:
                    try:
                        value = float(data[field])
                        if value < 0:
                            errors.append(f"{field} cannot be negative")
                        if value > 1e12:  # 1 trillion limit
                            errors.append(f"{field} value too large")
                    except (ValueError, TypeError):
                        errors.append(f"{field} must be a valid number")
            
            # Validate data types
            valid_data_types = ['income', 'expense', 'investment', 'loan', 'insurance', 'tax']
            if 'data_type' in data and data['data_type'] not in valid_data_types:
                errors.append(f"Invalid data_type. Must be one of: {', '.join(valid_data_types)}")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Financial data validation failed: {e}")
            return False, [f"Validation error: {str(e)}"]
    
    def log_security_event(self, event_type: str, user_id: str = None, details: Dict = None):
        """Log security events for monitoring"""
        try:
            security_log = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': event_type,
                'user_id': user_id,
                'details': details or {},
                'severity': self._get_event_severity(event_type)
            }
            
            # In production, send to security monitoring system
            self.logger.info(f"Security event: {json.dumps(security_log)}")
            
        except Exception as e:
            self.logger.error(f"Failed to log security event: {e}")
    
    def _get_event_severity(self, event_type: str) -> str:
        """Get severity level for security events"""
        high_severity = ['login_failure', 'rate_limit_exceeded', 'invalid_token', 'injection_attempt']
        medium_severity = ['password_change', 'profile_update', 'data_access']
        
        if event_type in high_severity:
            return 'HIGH'
        elif event_type in medium_severity:
            return 'MEDIUM'
        else:
            return 'LOW'
