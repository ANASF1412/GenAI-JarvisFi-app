"""
JarvisFi - Main FastAPI Application
Your AI-Powered Financial Genius
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import time
import logging
from typing import Dict, Any

# Core imports
from core.config import get_settings
from core.database import init_db, close_db
from core.cache import init_redis, close_redis
from core.logging import setup_logging
from core.security import SecurityManager

# API routes
from api.auth import router as auth_router
from api.chat import router as chat_router
from api.financial import router as financial_router
from api.voice import router as voice_router
from api.farmer import router as farmer_router
from api.community import router as community_router
from api.admin import router as admin_router

# Services
from services.ai_service import AIService
from services.translation_service import TranslationService
from services.voice_service import VoiceService

# Utilities
from utils.validators import validate_request
from utils.helpers import get_client_ip

# Initialize settings
settings = get_settings()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting JarvisFi - Your AI-Powered Financial Genius")
    
    try:
        # Initialize database
        await init_db()
        logger.info("✅ Database initialized")
        
        # Initialize Redis cache
        await init_redis()
        logger.info("✅ Redis cache initialized")
        
        # Initialize AI services
        ai_service = AIService()
        await ai_service.initialize()
        app.state.ai_service = ai_service
        logger.info("✅ AI services initialized")
        
        # Initialize translation service
        translation_service = TranslationService()
        await translation_service.initialize()
        app.state.translation_service = translation_service
        logger.info("✅ Translation service initialized")
        
        # Initialize voice service
        if settings.VOICE_INTERFACE_ENABLED:
            voice_service = VoiceService()
            await voice_service.initialize()
            app.state.voice_service = voice_service
            logger.info("✅ Voice service initialized")
        
        # Initialize security manager
        security_manager = SecurityManager()
        app.state.security_manager = security_manager
        logger.info("✅ Security manager initialized")
        
        logger.info("🎉 JarvisFi startup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down JarvisFi...")
    
    try:
        # Close database connections
        await close_db()
        logger.info("✅ Database connections closed")
        
        # Close Redis connections
        await close_redis()
        logger.info("✅ Redis connections closed")
        
        # Cleanup AI services
        if hasattr(app.state, 'ai_service'):
            await app.state.ai_service.cleanup()
            logger.info("✅ AI services cleaned up")
        
        # Cleanup translation service
        if hasattr(app.state, 'translation_service'):
            await app.state.translation_service.cleanup()
            logger.info("✅ Translation service cleaned up")
        
        # Cleanup voice service
        if hasattr(app.state, 'voice_service'):
            await app.state.voice_service.cleanup()
            logger.info("✅ Voice service cleaned up")
        
        logger.info("👋 JarvisFi shutdown completed")
        
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Create FastAPI application
app = FastAPI(
    title="JarvisFi API",
    description="Your AI-Powered Financial Genius - Comprehensive Financial Assistant API",
    version=settings.APP_VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["https://jarvisfi.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["jarvisfi.com", "*.jarvisfi.com"]
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log slow requests
    if process_time > 2.0:
        logger.warning(f"Slow request: {request.url} took {process_time:.2f}s")
    
    return response


# Rate limiting middleware
@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    """Basic rate limiting middleware"""
    client_ip = get_client_ip(request)
    
    # TODO: Implement proper rate limiting with Redis
    # For now, just log the request
    logger.debug(f"Request from {client_ip}: {request.method} {request.url}")
    
    response = await call_next(request)
    return response


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Global HTTP exception handler"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc} - {request.url}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": time.time(),
        "services": {
            "database": "healthy",  # TODO: Add actual health checks
            "redis": "healthy",
            "ai_service": "healthy"
        }
    }


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "description": settings.APP_DESCRIPTION,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(financial_router, prefix="/api/v1/financial", tags=["Financial"])
app.include_router(voice_router, prefix="/api/v1/voice", tags=["Voice"])
app.include_router(farmer_router, prefix="/api/v1/farmer", tags=["Farmer"])
app.include_router(community_router, prefix="/api/v1/community", tags=["Community"])
app.include_router(admin_router, prefix="/api/v1/admin", tags=["Admin"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
