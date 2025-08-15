# app/schemas/sr_fct_items.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, DECIMAL
from datetime import datetime
from typing import TYPE_CHECKING


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrFctItemsBase(BaseSchema):
    appkey: str
    keyid: Optional[str] = None
    matnr: Optional[str] = None
    fk_actiontype: Optional[int] = None
    discount: DECIMAL = DECIMAL("0.00")
    qty: int = 0
    srp: Optional[DECIMAL] = None
    total_amount: Optional[DECIMAL] = None
    net_price: Optional[DECIMAL] = None
    net_total_amount: Optional[DECIMAL] = None
    fsp_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    dr_number: Optional[str] = None
    dr_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
    code: Optional[str] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    rsmemail: Optional[str] = None
    fspemail: Optional[str] = None
    is_sdo: Optional[int] = None


class SrFctItemsCreate(SrFctItemsBase):
    """Schema for creating new SR item records"""

    pass


class SrFctItems(SrFctItemsBase):
    """Base schema for SR item responses"""

    id: int


if TYPE_CHECKING:
    from .dimensions import DimMara, DimCustomDropdown
    from .sr_fct_header import SrFctHeader
    from .sr_fct_logsremarksitems import SrFctLogsRemarksItems


class SrFctItemsComplete(SrFctItems):
    """Complete schema including all relationships"""

    header: Optional["SrFctHeader"] = None
    material: Optional["DimMara"] = None
    action_type: Optional["DimCustomDropdown"] = None
    item_logs: List["SrFctLogsRemarksItems"] = []


class SrFctItemsResponse(SrFctItems):
    """Standard response schema for SR items"""

    pass


class SrFctItemsDetailResponse(SrFctItemsComplete):
    """Detailed response schema with relationships"""

    pass


class SrFctItemsListResponse(BaseSchema):
    """Paginated list response for SR items"""

    items: List[SrFctItems]
    total: int
    skip: int
    limit: int
