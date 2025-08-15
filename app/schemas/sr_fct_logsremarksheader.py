from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from typing import TYPE_CHECKING


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrFctLogsRemarksHeaderBase(BaseSchema):
    appkey: str
    keyid: Optional[str] = None
    fk_typeapprovalstatus: Optional[int] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
    type_remarks: Optional[str] = None
    created_by: Optional[str] = None


class SrFctLogsRemarksHeaderCreate(SrFctLogsRemarksHeaderBase):
    """Schema for creating new header log records"""

    pass


class SrFctLogsRemarksHeader(SrFctLogsRemarksHeaderBase):
    """Base schema for header log responses"""

    id: int


if TYPE_CHECKING:
    from .dimensions import SrDimTypeOfApprovalStat
    from .sr_fct_header import SrFctHeader


class SrFctLogsRemarksHeaderComplete(SrFctLogsRemarksHeader):
    """Complete schema including all relationships"""

    header: Optional["SrFctHeader"] = None
    approval_status: Optional["SrDimTypeOfApprovalStat"] = None


class SrFctLogsRemarksHeaderResponse(SrFctLogsRemarksHeader):
    """Standard response schema for header logs"""

    pass


class SrFctLogsRemarksHeaderDetailResponse(SrFctLogsRemarksHeaderComplete):
    """Detailed response schema with relationships"""

    pass


class SrFctLogsRemarksHeaderListResponse(BaseSchema):
    """Paginated list response for header logs"""

    items: List[SrFctLogsRemarksHeader]
    total: int
    skip: int
    limit: int
