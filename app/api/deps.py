# app/api/deps.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, DatabaseError, OperationalError
from typing import Generator
from fastapi import Request
import logging
import uuid

from app.db.database import get_db
from app.core.config import get_settings
from app.core.exceptions import DatabaseException, BaseCustomException

settings = get_settings()
logger = logging.getLogger(__name__)


def get_db_session() -> Generator[Session, None, None]:
    """
    Database session dependency with proper error handling
    Only catches actual database connection/infrastructure errors
    """
    db = None
    try:
        logger.debug("Creating database session")
        db = next(get_db())
        yield db
        logger.debug("Database session completed successfully")
        
    except BaseCustomException:
        # These are business logic exceptions
        if db:
            try:
                db.rollback()
            except Exception:
                pass
        raise
        
    except (DatabaseError, OperationalError) as e:
        # These are actual database connection/server issues
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        if db:
            try:
                db.rollback()
            except Exception:
                pass
        raise DatabaseException("Database connection failed", details=str(e))
        
    except SQLAlchemyError as e:
        # Other SQLAlchemy errors - could be configuration issues
        logger.error(f"SQLAlchemy error: {str(e)}", exc_info=True)
        if db:
            try:
                db.rollback()
            except Exception:
                pass
        raise DatabaseException("Database query failed", details=str(e))
        
    except Exception as e:
        # Any other unexpected errors (not business logic)
        logger.error(f"Unexpected database session error: {type(e).__name__}: {str(e)}", exc_info=True)
        if db:
            try:
                db.rollback()
            except Exception:
                pass
        raise DatabaseException("Unexpected database error", details=f"{type(e).__name__}: {str(e)}")
        
    finally:
        if db:
            try:
                logger.debug("Closing database session")
                db.close()
            except Exception as e:
                logger.warning(f"Error closing database session: {str(e)}")


def get_request_id(request: Request) -> str:
    """Get request ID from request state with fallback"""
    request_id = getattr(request.state, 'request_id', None)
    if not request_id:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        logger.warning("Request ID was missing, generated fallback")
    return request_id


def get_current_settings():
    """Settings dependency"""
    return get_settings()