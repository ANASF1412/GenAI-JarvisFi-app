"""
JarvisFi - Configuration Management
Centralized configuration for the entire application
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional, Dict, Any
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application Settings
    APP_NAME: str = Field(default="JarvisFi", description="Application name")
    APP_VERSION: str = Field(default="2.0.0", description="Application version")
    APP_DESCRIPTION: str = Field(default="Your AI-Powered Financial Genius", description="Application description")
    DEBUG: bool = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    ENVIRONMENT: str = Field(default="production", description="Environment")
    
    # Security
    SECRET_KEY: str = Field(..., description="Secret key for JWT")
    JWT_SECRET_KEY: str = Field(..., description="JWT secret key")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    JWT_EXPIRE_MINUTES: int = Field(default=30, description="JWT expiration in minutes")
    ENCRYPTION_KEY: str = Field(..., description="Encryption key")
    AES_KEY: str = Field(..., description="AES encryption key")
    
    # Database Configuration
    DATABASE_URL: str = Field(..., description="Database URL")
    POSTGRES_DB: str = Field(default="jarvisfi", description="PostgreSQL database name")
    POSTGRES_USER: str = Field(default="jarvisfi_user", description="PostgreSQL username")
    POSTGRES_PASSWORD: str = Field(..., description="PostgreSQL password")
    POSTGRES_HOST: str = Field(default="localhost", description="PostgreSQL host")
    POSTGRES_PORT: int = Field(default=5432, description="PostgreSQL port")
    
    # Redis Configuration
    REDIS_URL: str = Field(..., description="Redis URL")
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    
    # MongoDB Configuration
    MONGODB_URL: str = Field(..., description="MongoDB URL")
    MONGODB_HOST: str = Field(default="localhost", description="MongoDB host")
    MONGODB_PORT: int = Field(default=27017, description="MongoDB port")
    MONGODB_USERNAME: Optional[str] = Field(default=None, description="MongoDB username")
    MONGODB_PASSWORD: Optional[str] = Field(default=None, description="MongoDB password")
    MONGODB_DATABASE: str = Field(default="jarvisfi_docs", description="MongoDB database name")
    
    # IBM Watson Configuration
    IBM_WATSON_API_KEY: Optional[str] = Field(default=None, description="IBM Watson API key")
    IBM_WATSON_URL: Optional[str] = Field(default=None, description="IBM Watson URL")
    IBM_WATSON_ASSISTANT_ID: Optional[str] = Field(default=None, description="IBM Watson Assistant ID")
    IBM_WATSONX_PROJECT_ID: Optional[str] = Field(default=None, description="IBM WatsonX Project ID")
    IBM_WATSONX_API_KEY: Optional[str] = Field(default=None, description="IBM WatsonX API key")
    
    # Hugging Face Configuration
    HUGGINGFACE_API_KEY: Optional[str] = Field(default=None, description="Hugging Face API key")
    HUGGINGFACE_MODEL_CACHE_DIR: str = Field(default="./models/huggingface", description="HF model cache directory")
    
    # OpenAI Configuration (Backup)
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API key")
    OPENAI_MODEL: str = Field(default="gpt-3.5-turbo", description="OpenAI model")
    
    # Translation Models
    TRANSLATION_MODEL_EN_TA: str = Field(default="Helsinki-NLP/opus-mt-en-mul", description="English to Tamil model")
    TRANSLATION_MODEL_EN_HI: str = Field(default="Helsinki-NLP/opus-mt-en-hi", description="English to Hindi model")
    TRANSLATION_MODEL_EN_TE: str = Field(default="Helsinki-NLP/opus-mt-en-mul", description="English to Telugu model")
    TRANSLATION_CACHE_SIZE: int = Field(default=1000, description="Translation cache size")
    
    # Voice Processing
    TTS_MODEL: str = Field(default="tts_models/multilingual/multi-dataset/xtts_v2", description="TTS model")
    STT_MODEL: str = Field(default="openai/whisper-base", description="STT model")
    VOICE_CACHE_DIR: str = Field(default="./cache/voice", description="Voice cache directory")
    AUDIO_SAMPLE_RATE: int = Field(default=22050, description="Audio sample rate")
    
    # Financial APIs
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None, description="Alpha Vantage API key")
    XE_CURRENCY_API_KEY: Optional[str] = Field(default=None, description="XE Currency API key")
    YAHOO_FINANCE_ENABLED: bool = Field(default=True, description="Enable Yahoo Finance")
    
    # Credit Score APIs
    CIBIL_API_KEY: Optional[str] = Field(default=None, description="CIBIL API key")
    CIBIL_API_URL: str = Field(default="https://api.cibil.com/v1", description="CIBIL API URL")
    EXPERIAN_API_KEY: Optional[str] = Field(default=None, description="Experian API key")
    EXPERIAN_API_URL: str = Field(default="https://api.experian.com/v1", description="Experian API URL")
    
    # Government APIs
    RBI_API_URL: str = Field(default="https://api.rbi.org.in", description="RBI API URL")
    SEBI_API_URL: str = Field(default="https://api.sebi.gov.in", description="SEBI API URL")
    UIDAI_API_KEY: Optional[str] = Field(default=None, description="UIDAI API key")
    
    # Weather API (for Farmers)
    WEATHER_API_KEY: Optional[str] = Field(default=None, description="Weather API key")
    WEATHER_API_URL: str = Field(default="https://api.openweathermap.org/data/2.5", description="Weather API URL")
    
    # Geolocation
    GEOLOCATION_API_KEY: Optional[str] = Field(default=None, description="Geolocation API key")
    GOOGLE_MAPS_API_KEY: Optional[str] = Field(default=None, description="Google Maps API key")
    
    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP host")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_USERNAME: Optional[str] = Field(default=None, description="SMTP username")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="SMTP password")
    EMAIL_FROM: str = Field(default="noreply@jarvisfi.com", description="Email from address")
    
    # SMS Configuration
    SMS_API_KEY: Optional[str] = Field(default=None, description="SMS API key")
    SMS_API_URL: Optional[str] = Field(default=None, description="SMS API URL")
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, description="Google OAuth client ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, description="Google OAuth client secret")
    FACEBOOK_CLIENT_ID: Optional[str] = Field(default=None, description="Facebook OAuth client ID")
    FACEBOOK_CLIENT_SECRET: Optional[str] = Field(default=None, description="Facebook OAuth client secret")
    
    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", description="Upload directory")
    MAX_FILE_SIZE: int = Field(default=10485760, description="Max file size in bytes (10MB)")
    ALLOWED_EXTENSIONS: str = Field(default="pdf,doc,docx,xls,xlsx,jpg,jpeg,png", description="Allowed file extensions")
    
    # Performance Settings
    MAX_WORKERS: int = Field(default=4, description="Maximum worker threads")
    CACHE_TTL: int = Field(default=3600, description="Cache TTL in seconds")
    REQUEST_TIMEOUT: int = Field(default=30, description="Request timeout in seconds")
    MAX_CONNECTIONS: int = Field(default=100, description="Maximum connections")
    MEMORY_LIMIT: int = Field(default=512, description="Memory limit in MB")
    
    # Monitoring
    PROMETHEUS_PORT: int = Field(default=9090, description="Prometheus port")
    GRAFANA_PORT: int = Field(default=3000, description="Grafana port")
    LOG_FILE: str = Field(default="./logs/jarvisfi.log", description="Log file path")
    METRICS_ENABLED: bool = Field(default=True, description="Enable metrics")
    
    # Feature Flags
    VOICE_INTERFACE_ENABLED: bool = Field(default=True, description="Enable voice interface")
    MULTILINGUAL_ENABLED: bool = Field(default=True, description="Enable multilingual support")
    FARMER_TOOLS_ENABLED: bool = Field(default=True, description="Enable farmer tools")
    COMMUNITY_FORUM_ENABLED: bool = Field(default=True, description="Enable community forum")
    GAMIFICATION_ENABLED: bool = Field(default=True, description="Enable gamification")
    FRAUD_DETECTION_ENABLED: bool = Field(default=True, description="Enable fraud detection")
    BIOMETRIC_AUTH_ENABLED: bool = Field(default=False, description="Enable biometric authentication")
    OFFLINE_MODE_ENABLED: bool = Field(default=True, description="Enable offline mode")
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Rate limit per minute")
    RATE_LIMIT_PER_HOUR: int = Field(default=1000, description="Rate limit per hour")
    RATE_LIMIT_PER_DAY: int = Field(default=10000, description="Rate limit per day")
    
    # Backup Configuration
    BACKUP_ENABLED: bool = Field(default=True, description="Enable backups")
    BACKUP_SCHEDULE: str = Field(default="0 2 * * *", description="Backup schedule (cron)")
    BACKUP_RETENTION_DAYS: int = Field(default=30, description="Backup retention in days")
    BACKUP_STORAGE_PATH: str = Field(default="./backups", description="Backup storage path")
    
    # Compliance
    GDPR_COMPLIANCE: bool = Field(default=True, description="GDPR compliance")
    HIPAA_COMPLIANCE: bool = Field(default=True, description="HIPAA compliance")
    DATA_RETENTION_DAYS: int = Field(default=2555, description="Data retention in days (7 years)")
    AUDIT_LOG_ENABLED: bool = Field(default=True, description="Enable audit logging")
    
    # Localization
    DEFAULT_LANGUAGE: str = Field(default="en", description="Default language")
    SUPPORTED_LANGUAGES: str = Field(default="en,ta,hi,te", description="Supported languages")
    TIMEZONE: str = Field(default="Asia/Kolkata", description="Default timezone")
    CURRENCY: str = Field(default="INR", description="Default currency")
    
    # Analytics
    GOOGLE_ANALYTICS_ID: Optional[str] = Field(default=None, description="Google Analytics ID")
    MIXPANEL_TOKEN: Optional[str] = Field(default=None, description="Mixpanel token")
    ANALYTICS_ENABLED: bool = Field(default=True, description="Enable analytics")
    
    @validator("SUPPORTED_LANGUAGES")
    def validate_supported_languages(cls, v):
        """Validate supported languages"""
        languages = v.split(",")
        valid_languages = ["en", "ta", "hi", "te", "bn", "gu", "kn", "ml", "mr", "or", "pa", "ur"]
        for lang in languages:
            if lang not in valid_languages:
                raise ValueError(f"Unsupported language: {lang}")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {v}")
        return v.upper()
    
    @property
    def supported_languages_list(self) -> List[str]:
        """Get supported languages as list"""
        return self.SUPPORTED_LANGUAGES.split(",")
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Get allowed extensions as list"""
        return self.ALLOWED_EXTENSIONS.split(",")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Create directories if they don't exist
def create_directories():
    """Create necessary directories"""
    settings = get_settings()
    
    directories = [
        settings.UPLOAD_DIR,
        settings.VOICE_CACHE_DIR,
        settings.HUGGINGFACE_MODEL_CACHE_DIR,
        settings.BACKUP_STORAGE_PATH,
        Path(settings.LOG_FILE).parent,
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


# Initialize directories on import
create_directories()
