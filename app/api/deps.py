# app/api/deps.py
from sqlalchemy.orm import Session
from typing import Generator

from app.db.database import get_db
from app.core.config import get_settings

settings = get_settings()


def get_db_session() -> Generator[Session, None, None]:
    """
    Database session dependency
    """
    yield from get_db()
