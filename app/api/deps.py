# app/deps.py
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session
from typing import Generator, Optional

from app.db.database import get_db
from app.schemas.base import PaginationParams
from app.core.config import get_settings

settings = get_settings()


def get_db_session() -> Generator[Session, None, None]:
    """
    Database session dependency
    """
    yield from get_db()


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(
        20, ge=1, le=settings.MAX_PAGE_SIZE, description="Items per page"
    ),
) -> PaginationParams:
    """
    Common pagination parameters dependency
    """
    return PaginationParams(page=page, size=size)


def validate_page_size(size: int) -> int:
    """
    Validate and limit page size
    """
    if size > settings.MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=400, detail=f"Page size cannot exceed {settings.MAX_PAGE_SIZE}"
        )
    return size


# Common query parameters for filtering
def get_common_filters(
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: Optional[str] = Query(
        "asc", regex="^(asc|desc)$", description="Sort order"
    ),
) -> dict:
    """
    Common filtering parameters
    """
    return {"search": search, "sort_by": sort_by, "sort_order": sort_order}
