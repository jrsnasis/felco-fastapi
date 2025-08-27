# app/schemas/base.py - CLEANED VERSION
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configurations"""

    model_config = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True, str_strip_whitespace=True
    )


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response format"""

    success: bool = Field(
        default=True, description="Indicates if the request was successful"
    )
    status_code: int = Field(default=200, description="HTTP status code")
    message: str = Field(description="Human-readable success message")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Response timestamp"
    )
    data: T = Field(description="Response data")
    count: Optional[int] = Field(
        default=None, description="Number of records returned (for lists)"
    )

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
