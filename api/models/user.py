"""
JarvisFi - User Models
Database models for user management and authentication
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Enum as SQLEnum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from datetime import datetime
from typing import Dict, Any, Optional, List

from core.database import Base


class UserType(enum.Enum):
    """User type enumeration"""
    STUDENT = "student"
    PROFESSIONAL = "professional"
    FARMER = "farmer"
    SENIOR_CITIZEN = "senior_citizen"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class UserStatus(enum.Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
    DELETED = "deleted"


class AuthProvider(enum.Enum):
    """Authentication provider enumeration"""
    LOCAL = "local"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    AADHAAR = "aadhaar"
    BIOMETRIC = "biometric"


class User(Base):
    """Main user model"""
    __tablename__ = "users"
    
    # Primary fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    username = Column(String(50), unique=True, index=True, nullable=True)
    
    # Authentication
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    
    # User categorization
    user_type = Column(SQLEnum(UserType), default=UserType.BEGINNER, nullable=False)
    user_status = Column(SQLEnum(UserStatus), default=UserStatus.PENDING_VERIFICATION, nullable=False)
    
    # Preferences
    preferred_language = Column(String(10), default="en", nullable=False)
    preferred_currency = Column(String(10), default="INR", nullable=False)
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    
    # Location
    country = Column(String(100), default="India", nullable=False)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    
    # Financial profile
    monthly_income = Column(Float, nullable=True)
    occupation = Column(String(100), nullable=True)
    employer = Column(String(200), nullable=True)
    
    # KYC information (encrypted)
    pan_number = Column(String(255), nullable=True)  # Encrypted
    aadhaar_number = Column(String(255), nullable=True)  # Encrypted
    kyc_status = Column(String(20), default="pending", nullable=False)
    kyc_verified_at = Column(DateTime, nullable=True)
    
    # Security
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    biometric_enabled = Column(Boolean, default=False, nullable=False)
    last_login = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    
    # Preferences and settings
    settings = Column(JSON, default=dict, nullable=False)
    privacy_settings = Column(JSON, default=dict, nullable=False)
    notification_preferences = Column(JSON, default=dict, nullable=False)
    
    # Gamification
    points = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    badges = Column(JSON, default=list, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Soft delete
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    auth_providers = relationship("UserAuthProvider", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    financial_profiles = relationship("FinancialProfile", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, type={self.user_type})>"
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_farmer(self) -> bool:
        """Check if user is a farmer"""
        return self.user_type == UserType.FARMER
    
    @property
    def is_senior_citizen(self) -> bool:
        """Check if user is a senior citizen"""
        return self.user_type == UserType.SENIOR_CITIZEN
    
    @property
    def age(self) -> Optional[int]:
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get user setting"""
        return self.settings.get(key, default)
    
    def set_setting(self, key: str, value: Any):
        """Set user setting"""
        if self.settings is None:
            self.settings = {}
        self.settings[key] = value
    
    def add_points(self, points: int, reason: str = ""):
        """Add gamification points"""
        self.points += points
        # Level up logic
        if self.points >= (self.level * 100):
            self.level += 1
    
    def add_badge(self, badge: str):
        """Add badge to user"""
        if self.badges is None:
            self.badges = []
        if badge not in self.badges:
            self.badges.append(badge)


class UserAuthProvider(Base):
    """User authentication providers"""
    __tablename__ = "user_auth_providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    provider = Column(SQLEnum(AuthProvider), nullable=False)
    provider_id = Column(String(255), nullable=False)
    provider_data = Column(JSON, default=dict)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="auth_providers")
    
    def __repr__(self):
        return f"<UserAuthProvider(user_id={self.user_id}, provider={self.provider})>"


class UserSession(Base):
    """User session management"""
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True, nullable=True, index=True)
    
    # Session details
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    device_info = Column(JSON, default=dict)
    location_info = Column(JSON, default=dict)
    
    # Session status
    is_active = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(user_id={self.user_id}, active={self.is_active})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if session is expired"""
        return datetime.utcnow() > self.expires_at


class UserPreference(Base):
    """User preferences and settings"""
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # ui, notifications, privacy, etc.
    key = Column(String(100), nullable=False)
    value = Column(JSON, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, key={self.key})>"


class UserActivity(Base):
    """User activity tracking"""
    __tablename__ = "user_activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    activity_type = Column(String(50), nullable=False, index=True)
    activity_data = Column(JSON, default=dict)
    
    # Context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    session_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<UserActivity(user_id={self.user_id}, type={self.activity_type})>"
