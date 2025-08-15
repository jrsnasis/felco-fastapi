from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from typing import TYPE_CHECKING


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrFctAttachmentBase(BaseSchema):
    appkey: str
    keyid: Optional[str] = None
    image: Optional[str] = None
    image_tag: Optional[str] = None
    is_active: Optional[bool] = None
    table_name: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
    upload_state: Optional[int] = None
    uploaded_by: Optional[str] = None


class SrFctAttachmentCreate(SrFctAttachmentBase):
    """Schema for creating new attachment records"""

    pass


class SrFctAttachment(SrFctAttachmentBase):
    """Base schema for attachment responses"""

    id: int


if TYPE_CHECKING:
    from .sr_fct_header import SrFctHeader


class SrFctAttachmentComplete(SrFctAttachment):
    """Complete schema including header relationship"""

    header: Optional["SrFctHeader"] = None


class SrFctAttachmentResponse(SrFctAttachment):
    """Standard response schema for attachments"""

    pass


class SrFctAttachmentDetailResponse(SrFctAttachmentComplete):
    """Detailed response schema with relationships"""

    pass


class SrFctAttachmentListResponse(BaseSchema):
    """Paginated list response for attachments"""

    items: List[SrFctAttachment]
    total: int
    skip: int
    limit: int
