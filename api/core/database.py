"""
JarvisFi - Database Management
SQLAlchemy database configuration and management
"""

from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import asynccontextmanager
import asyncio
import logging
from typing import AsyncGenerator, Optional

from .config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Database engine
engine = None
SessionLocal = None
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


def create_database_engine():
    """Create database engine with proper configuration"""
    global engine, SessionLocal
    
    try:
        # Create engine with connection pooling
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20,
            echo=settings.DEBUG,
            connect_args={
                "options": "-c timezone=Asia/Kolkata"
            } if "postgresql" in settings.DATABASE_URL else {}
        )
        
        # Create session factory
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
        
        logger.info("✅ Database engine created successfully")
        return engine
        
    except Exception as e:
        logger.error(f"❌ Failed to create database engine: {e}")
        raise


def get_db() -> Session:
    """Get database session"""
    if SessionLocal is None:
        create_database_engine()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_async_db() -> AsyncGenerator[Session, None]:
    """Get async database session"""
    if SessionLocal is None:
        create_database_engine()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database"""
    try:
        # Create engine if not exists
        if engine is None:
            create_database_engine()
        
        # Import all models to ensure they are registered
        from models import user, financial, chat, farmer, community
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        logger.info("✅ Database initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db():
    """Close database connections"""
    global engine
    
    try:
        if engine:
            engine.dispose()
            logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")


def check_db_health() -> bool:
    """Check database health"""
    try:
        if engine is None:
            return False
        
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Database event listeners
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance"""
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()


@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log slow queries"""
    if settings.DEBUG:
        context._query_start_time = asyncio.get_event_loop().time()


@event.listens_for(engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log query execution time"""
    if settings.DEBUG and hasattr(context, '_query_start_time'):
        total = asyncio.get_event_loop().time() - context._query_start_time
        if total > 0.1:  # Log queries taking more than 100ms
            logger.warning(f"Slow query ({total:.3f}s): {statement[:100]}...")


class DatabaseManager:
    """Database manager for advanced operations"""
    
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    async def execute_raw_query(self, query: str, params: Optional[dict] = None):
        """Execute raw SQL query"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(query, params or {})
                return result.fetchall()
        except Exception as e:
            logger.error(f"Raw query execution failed: {e}")
            raise
    
    async def backup_database(self, backup_path: str):
        """Create database backup"""
        try:
            # Implementation depends on database type
            if "postgresql" in settings.DATABASE_URL:
                import subprocess
                cmd = [
                    "pg_dump",
                    settings.DATABASE_URL,
                    "-f", backup_path
                ]
                subprocess.run(cmd, check=True)
            
            logger.info(f"Database backup created: {backup_path}")
            
        except Exception as e:
            logger.error(f"Database backup failed: {e}")
            raise
    
    async def restore_database(self, backup_path: str):
        """Restore database from backup"""
        try:
            # Implementation depends on database type
            if "postgresql" in settings.DATABASE_URL:
                import subprocess
                cmd = [
                    "psql",
                    settings.DATABASE_URL,
                    "-f", backup_path
                ]
                subprocess.run(cmd, check=True)
            
            logger.info(f"Database restored from: {backup_path}")
            
        except Exception as e:
            logger.error(f"Database restore failed: {e}")
            raise
    
    async def get_database_stats(self) -> dict:
        """Get database statistics"""
        try:
            stats = {}
            
            # Get table sizes
            if "postgresql" in settings.DATABASE_URL:
                query = """
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation
                FROM pg_stats
                WHERE schemaname = 'public'
                """
                result = await self.execute_raw_query(query)
                stats["table_stats"] = result
            
            # Get connection count
            with self.engine.connect() as conn:
                if "postgresql" in settings.DATABASE_URL:
                    result = conn.execute("SELECT count(*) FROM pg_stat_activity")
                    stats["active_connections"] = result.scalar()
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {}
    
    async def optimize_database(self):
        """Optimize database performance"""
        try:
            if "postgresql" in settings.DATABASE_URL:
                with self.engine.connect() as conn:
                    # Analyze tables
                    conn.execute("ANALYZE")
                    # Vacuum tables
                    conn.execute("VACUUM")
            
            logger.info("Database optimization completed")
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            raise


# Global database manager instance
db_manager = DatabaseManager()
