# app/schemas/base.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Generic, TypeVar, List
from datetime import datetime

# Generic type for paginated responses
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configurations"""

    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, str_strip_whitespace=True
    )


class TimestampMixin(BaseModel):
    """Mixin for models with timestamps"""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PaginationParams(BaseModel):
    """Standard pagination parameters"""

    page: int = 1
    size: int = 20

    model_config = ConfigDict(json_schema_extra={"example": {"page": 1, "size": 20}})


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response"""

    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(
        cls, items: List[T], total: int, page: int, size: int
    ) -> "PaginatedResponse[T]":
        pages = (total + size - 1) // size
        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )


class ResponseMessage(BaseModel):
    """Standard response message"""

    message: str
    success: bool = True
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response"""

    message: str
    success: bool = False
    error_code: Optional[str] = None
    details: Optional[dict] = None
