from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, List
from datetime import datetime

from pydantic import field_validator
from typing import Optional


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PaginationParams(BaseSchema):
    """Standard pagination parameters"""

    skip: int = 0
    limit: int = 100


T = TypeVar("T")


class PaginatedResponse(BaseSchema, Generic[T]):
    """Generic paginated response"""

    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool = False
    has_previous: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self.has_next = (self.skip + self.limit) < self.total
        self.has_previous = self.skip > 0


class DateRangeFilter(BaseSchema):
    """Date range filter for queries"""

    start_date: datetime
    end_date: datetime


class SrHeaderFilter(BaseSchema):
    """Filter parameters for SR Header queries"""

    fk_status: Optional[int] = None
    fk_typerequest: Optional[int] = None
    kunnr: Optional[str] = None
    code: Optional[str] = None
    date_range: Optional[DateRangeFilter] = None
    created_by: Optional[str] = None


class VisitsFilter(BaseSchema):
    """Filter parameters for Visits queries"""

    kunnr: Optional[str] = None
    code: Optional[str] = None
    vtype: Optional[str] = None
    date_range: Optional[DateRangeFilter] = None
    empid: Optional[int] = None


class ResponseStatus(BaseSchema):
    """Standard API response status"""

    success: bool
    message: str
    timestamp: datetime = datetime.utcnow()


class ErrorResponse(ResponseStatus):
    """Error response schema"""

    error_code: Optional[str] = None
    details: Optional[dict] = None


class SuccessResponse(ResponseStatus):
    """Success response schema"""

    data: Optional[dict] = None


class BulkCreateResult(BaseSchema):
    """Result schema for bulk create operations"""

    created_count: int
    failed_count: int
    errors: List[str] = []


class BulkUpdateResult(BaseSchema):
    """Result schema for bulk update operations"""

    updated_count: int
    failed_count: int
    errors: List[str] = []


class BulkDeleteResult(BaseSchema):
    """Result schema for bulk delete operations"""

    deleted_count: int
    failed_count: int
    errors: List[str] = []


class EmailValidationMixin(BaseSchema):
    """Mixin for email field validation"""

    @field_validator("fspemail", "rsmemail", "gsmemail", "nsmemail", mode="before")
    @classmethod
    def validate_email(cls, v):
        if v and v.strip():
            # Basic email validation
            if "@" not in v:
                raise ValueError("Invalid email format")
        return v


class DECIMALValidationMixin(BaseSchema):
    """Mixin for DECIMAL field validation"""

    @field_validator("*", mode="before")
    @classmethod
    def validate_DECIMAL_fields(cls, v, info):
        if info.field_name and any(
            term in info.field_name.lower()
            for term in [
                "amount",
                "total",
                "price",
                "discount",
                "kbetr",
                "sales",
                "expense",
            ]
        ):
            if v is not None and v < 0:
                raise ValueError(f"{info.field_name} cannot be negative")
        return v


class AuditSchemaMixin(BaseSchema):
    """Mixin for audit fields"""

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None


class MobileAuditSchemaMixin(BaseSchema):
    """Mixin for mobile audit fields"""

    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
