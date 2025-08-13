"""
JarvisFi - Logging Configuration
Comprehensive logging setup for monitoring and debugging
"""

import logging
import logging.handlers
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import traceback

from .config import get_settings

settings = get_settings()


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": traceback.format_exception(*record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'user_id'):
            log_entry["user_id"] = record.user_id
        
        if hasattr(record, 'request_id'):
            log_entry["request_id"] = record.request_id
        
        if hasattr(record, 'ip_address'):
            log_entry["ip_address"] = record.ip_address
        
        return json.dumps(log_entry, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors"""
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Format message
        message = super().format(record)
        
        return f"{color}[{timestamp}] {record.levelname:8} {record.name:20} | {message}{reset}"


class SecurityFilter(logging.Filter):
    """Filter for security-related logs"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter security events"""
        security_keywords = [
            'login', 'logout', 'authentication', 'authorization',
            'password', 'token', 'security', 'fraud', 'suspicious'
        ]
        
        message = record.getMessage().lower()
        return any(keyword in message for keyword in security_keywords)


class PerformanceFilter(logging.Filter):
    """Filter for performance-related logs"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter performance events"""
        performance_keywords = [
            'slow', 'performance', 'latency', 'timeout',
            'memory', 'cpu', 'database', 'cache'
        ]
        
        message = record.getMessage().lower()
        return any(keyword in message for keyword in performance_keywords)


def setup_logging():
    """Setup comprehensive logging configuration"""
    
    # Create logs directory
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler with colored output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO if not settings.DEBUG else logging.DEBUG)
    console_formatter = ColoredFormatter()
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for general logs
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = JSONFormatter()
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)
    
    # Security log handler
    security_log_file = log_dir / "security.log"
    security_handler = logging.handlers.RotatingFileHandler(
        security_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(file_formatter)
    security_handler.addFilter(SecurityFilter())
    
    # Security logger
    security_logger = logging.getLogger("security")
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.INFO)
    security_logger.propagate = False
    
    # Performance log handler
    performance_log_file = log_dir / "performance.log"
    performance_handler = logging.handlers.RotatingFileHandler(
        performance_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    performance_handler.setLevel(logging.WARNING)
    performance_handler.setFormatter(file_formatter)
    performance_handler.addFilter(PerformanceFilter())
    
    # Performance logger
    performance_logger = logging.getLogger("performance")
    performance_logger.addHandler(performance_handler)
    performance_logger.setLevel(logging.WARNING)
    performance_logger.propagate = False
    
    # Error log handler
    error_log_file = log_dir / "error.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(file_formatter)
    root_logger.addHandler(error_handler)
    
    # Access log handler (for API requests)
    access_log_file = log_dir / "access.log"
    access_handler = logging.handlers.RotatingFileHandler(
        access_log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(file_formatter)
    
    # Access logger
    access_logger = logging.getLogger("access")
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False
    
    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    logging.info("✅ Logging configuration completed")


class LoggerAdapter(logging.LoggerAdapter):
    """Custom logger adapter with context"""
    
    def __init__(self, logger: logging.Logger, extra: Optional[Dict[str, Any]] = None):
        super().__init__(logger, extra or {})
    
    def process(self, msg: str, kwargs: Dict[str, Any]) -> tuple:
        """Process log message with extra context"""
        if 'extra' not in kwargs:
            kwargs['extra'] = {}
        
        kwargs['extra'].update(self.extra)
        return msg, kwargs


def get_logger(name: str, **context) -> LoggerAdapter:
    """Get logger with context"""
    logger = logging.getLogger(name)
    return LoggerAdapter(logger, context)


def log_api_request(method: str, path: str, status_code: int, 
                   response_time: float, user_id: Optional[str] = None,
                   ip_address: Optional[str] = None):
    """Log API request"""
    access_logger = logging.getLogger("access")
    
    log_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "response_time": response_time,
        "user_id": user_id,
        "ip_address": ip_address
    }
    
    access_logger.info("API_REQUEST", extra=log_data)


def log_security_event(event_type: str, user_id: Optional[str] = None, 
                      details: Optional[Dict[str, Any]] = None,
                      ip_address: Optional[str] = None):
    """Log security event"""
    security_logger = logging.getLogger("security")
    
    log_data = {
        "event_type": event_type,
        "user_id": user_id,
        "details": details or {},
        "ip_address": ip_address
    }
    
    security_logger.info("SECURITY_EVENT", extra=log_data)


def log_performance_issue(issue_type: str, details: Dict[str, Any]):
    """Log performance issue"""
    performance_logger = logging.getLogger("performance")
    
    log_data = {
        "issue_type": issue_type,
        "details": details
    }
    
    performance_logger.warning("PERFORMANCE_ISSUE", extra=log_data)


# Exception logging decorator
def log_exceptions(logger_name: str = None):
    """Decorator to log exceptions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name or func.__module__)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Exception in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator
