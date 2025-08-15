from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from typing import TYPE_CHECKING


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrFctLogsRemarksItemsBase(BaseSchema):
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


class SrFctLogsRemarksItemsCreate(SrFctLogsRemarksItemsBase):
    """Schema for creating new item log records"""

    pass


class SrFctLogsRemarksItems(SrFctLogsRemarksItemsBase):
    """Base schema for item log responses"""

    id: int


if TYPE_CHECKING:
    from .dimensions import SrDimTypeOfApprovalStat
    from .sr_fct_items import SrFctItems


class SrFctLogsRemarksItemsComplete(SrFctLogsRemarksItems):
    """Complete schema including all relationships"""

    item: Optional["SrFctItems"] = None
    approval_status: Optional["SrDimTypeOfApprovalStat"] = None


class SrFctLogsRemarksItemsResponse(SrFctLogsRemarksItems):
    """Standard response schema for item logs"""

    pass


class SrFctLogsRemarksItemsDetailResponse(SrFctLogsRemarksItemsComplete):
    """Detailed response schema with relationships"""

    pass


class SrFctLogsRemarksItemsListResponse(BaseSchema):
    """Paginated list response for item logs"""

    items: List[SrFctLogsRemarksItems]
    total: int
    skip: int
    limit: int
