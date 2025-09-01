# app/db/database.py
from sqlalchemy import create_engine, event, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Create engine with environment-specific settings
engine_kwargs = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "echo": settings.database_echo,
    "connect_args": {
        "connect_timeout": 60,
        "read_timeout": 60,
        "write_timeout": 60,
        "charset": "utf8mb4",
    },
}

# Production/Staging-specific optimizations
if settings.is_production() or settings.is_staging():
    engine_kwargs.update(
        {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_timeout": 30,
            "pool_recycle": 1800,
        }
    )
else:
    # Development settings
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


def verify_tables_with_retry(engine, base, max_retries=3, logger=logger):
    """Verify tables with retry logic for Railway deployment"""
    for attempt in range(max_retries):
        try:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            missing_tables = []

            for table in base.metadata.tables.keys():
                if table not in existing_tables:
                    missing_tables.append(table)

            if missing_tables:
                logger.warning(f"Missing tables detected: {missing_tables}")
            else:
                logger.info("All ORM tables verified successfully")
            return True

        except OperationalError as e:
            logger.warning(f"Database verification attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                import time

                time.sleep(5 * (attempt + 1))  # Exponential backoff
            else:
                logger.error(
                    f"Database verification failed after {max_retries} attempts"
                )
                raise e


# Update your verify_tables function
def verify_tables(engine, base, logger=logger):
    return verify_tables_with_retry(engine, base, logger=logger)
