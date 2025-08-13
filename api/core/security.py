"""
JarvisFi - Security Management
Comprehensive security utilities for authentication, encryption, and protection
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import secrets
import base64
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Union
import re

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encryption key derivation
def derive_key(password: str, salt: bytes) -> bytes:
    """Derive encryption key from password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


class SecurityManager:
    """Comprehensive security management"""
    
    def __init__(self):
        self.fernet = Fernet(settings.AES_KEY.encode() if len(settings.AES_KEY) == 44 else Fernet.generate_key())
        self.jwt_algorithm = settings.JWT_ALGORITHM
        self.jwt_secret = settings.JWT_SECRET_KEY
        self.jwt_expire_minutes = settings.JWT_EXPIRE_MINUTES
    
    # Password Management
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def generate_password(self, length: int = 12) -> str:
        """Generate secure random password"""
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        result = {
            "valid": True,
            "score": 0,
            "issues": []
        }
        
        # Length check
        if len(password) < 8:
            result["issues"].append("Password must be at least 8 characters long")
            result["valid"] = False
        else:
            result["score"] += 1
        
        # Uppercase check
        if not re.search(r"[A-Z]", password):
            result["issues"].append("Password must contain at least one uppercase letter")
            result["valid"] = False
        else:
            result["score"] += 1
        
        # Lowercase check
        if not re.search(r"[a-z]", password):
            result["issues"].append("Password must contain at least one lowercase letter")
            result["valid"] = False
        else:
            result["score"] += 1
        
        # Number check
        if not re.search(r"\d", password):
            result["issues"].append("Password must contain at least one number")
            result["valid"] = False
        else:
            result["score"] += 1
        
        # Special character check
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            result["issues"].append("Password must contain at least one special character")
            result["valid"] = False
        else:
            result["score"] += 1
        
        # Common password check
        common_passwords = ["password", "123456", "password123", "admin", "qwerty"]
        if password.lower() in common_passwords:
            result["issues"].append("Password is too common")
            result["valid"] = False
        
        return result
    
    # JWT Token Management
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.jwt_expire_minutes)
        
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            return None
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create refresh token"""
        data = {"sub": user_id, "type": "refresh"}
        expire = datetime.utcnow() + timedelta(days=30)  # 30 days for refresh token
        data.update({"exp": expire})
        
        return jwt.encode(data, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    # Data Encryption
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """Encrypt sensitive data"""
        if isinstance(data, str):
            data = data.encode()
        
        encrypted = self.fernet.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.fernet.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Invalid encrypted data")
    
    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data (one-way)"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    # API Key Management
    def generate_api_key(self, prefix: str = "jf") -> str:
        """Generate API key"""
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}_{random_part}"
    
    def validate_api_key_format(self, api_key: str) -> bool:
        """Validate API key format"""
        pattern = r"^[a-zA-Z0-9_-]+_[a-zA-Z0-9_-]{43}$"
        return bool(re.match(pattern, api_key))
    
    # Session Management
    def generate_session_id(self) -> str:
        """Generate secure session ID"""
        return secrets.token_urlsafe(32)
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    def validate_csrf_token(self, token: str, expected: str) -> bool:
        """Validate CSRF token"""
        return secrets.compare_digest(token, expected)
    
    # Input Validation and Sanitization
    def sanitize_input(self, input_data: str) -> str:
        """Sanitize user input"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_data)
        # Limit length
        sanitized = sanitized[:1000]
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate Indian phone number"""
        # Remove all non-digits
        digits = re.sub(r'\D', '', phone)
        
        # Check for valid Indian mobile number patterns
        patterns = [
            r'^[6-9]\d{9}$',  # 10 digits starting with 6-9
            r'^91[6-9]\d{9}$',  # With country code
            r'^0[6-9]\d{9}$'  # With leading 0
        ]
        
        return any(re.match(pattern, digits) for pattern in patterns)
    
    def validate_pan(self, pan: str) -> bool:
        """Validate PAN number format"""
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan.upper()))
    
    def validate_aadhaar(self, aadhaar: str) -> bool:
        """Validate Aadhaar number format"""
        # Remove spaces and hyphens
        digits = re.sub(r'[\s-]', '', aadhaar)
        
        # Check if it's 12 digits
        if not re.match(r'^\d{12}$', digits):
            return False
        
        # Aadhaar checksum validation (Verhoeff algorithm)
        return self._validate_aadhaar_checksum(digits)
    
    def _validate_aadhaar_checksum(self, aadhaar: str) -> bool:
        """Validate Aadhaar checksum using Verhoeff algorithm"""
        # Verhoeff algorithm implementation
        multiplication_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ]
        
        permutation_table = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ]
        
        check = 0
        for i, digit in enumerate(reversed(aadhaar)):
            check = multiplication_table[check][permutation_table[i % 8][int(digit)]]
        
        return check == 0
    
    # Security Headers
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers for HTTP responses"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
    
    # Audit Logging
    def log_security_event(self, event_type: str, user_id: Optional[str], details: Dict[str, Any]):
        """Log security events for audit"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details
        }
        
        # Log to security log file
        security_logger = logging.getLogger("security")
        security_logger.info(f"SECURITY_EVENT: {log_entry}")


# Global security manager instance
security_manager = SecurityManager()
