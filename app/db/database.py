# app/db/database.py
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Create engine with environment-specific settings
engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": settings.database_echo,
}

# Production-specific optimizations
if settings.is_production():
    engine_kwargs.update(
        {
            "poolclass": QueuePool,
            "pool_size": 20,
            "max_overflow": 30,
            "pool_timeout": 30,
            "pool_recycle": 1800,  # Shorter recycle time in production
        }
    )
else:
    # Development/staging settings
    engine_kwargs.update(
        {
            "pool_size": 5,
            "max_overflow": 10,
            "pool_timeout": 10,
        }
    )

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)


# Add connection event listeners for logging
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure database connection settings"""
    if not settings.is_production():
        logger.debug("Database connection established")


@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log connection checkout in development"""
    if settings.is_development():
        logger.debug("Connection checked out from pool")


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,  # Prevent lazy loading issues
)

# Create declarative base
Base = declarative_base()


# Dependency to get database session
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


# Database utilities
def test_database_connection():
    """Test database connectivity"""
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
            logger.info("Database connection test successful")
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False


# Health check function
async def get_database_status():
    """Get database status for health checks"""
    try:
        with engine.connect():
            return (
                {
                    "status": "healthy",
                    "connection_pool_size": engine.pool.size(),
                    "checked_out_connections": engine.pool.checkedout(),
                }
                if not settings.is_production()
                else {"status": "healthy"}
            )
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e) if not settings.is_production() else "Database error",
        }


def verify_tables(engine, base, logger=logger):
    """Verify that all ORM tables exist in the database (no creation)."""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    missing_tables = []

    for table in base.metadata.tables.keys():
        if table not in existing_tables:
            missing_tables.append(table)

    if missing_tables:
        logger.warning(f"Missing tables detected (not auto-created): {missing_tables}")
    else:
        logger.info("All ORM tables verified successfully (no creation attempted)")
