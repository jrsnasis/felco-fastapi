# app/schemas/sr_fct_header.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, DECIMAL
from datetime import datetime
from typing import TYPE_CHECKING
from pydantic import field_validator


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrFctHeaderBase(BaseSchema):
    appkey: str
    keyid: Optional[str] = None
    fk_typerequest: Optional[int] = None
    fk_reasonreturn: Optional[int] = None
    fk_modereturn: Optional[int] = None
    fk_status: Optional[int] = None
    kunnr: Optional[str] = None
    updated_shiptocode: Optional[str] = None
    ship_name: Optional[str] = None
    ship_to: Optional[str] = None
    sdo_pao_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    approver_remarks: Optional[str] = None
    return_total: Optional[DECIMAL] = None
    replacement_total: Optional[DECIMAL] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    rsmemail: Optional[str] = None
    fspemail: Optional[str] = None
    code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    m_created_at: Optional[datetime] = None
    m_updated_at: Optional[datetime] = None
    date_submitted_ssa: Optional[datetime] = None
    date_sent_approval: Optional[datetime] = None
    fsp: Optional[str] = None
    rsm: Optional[str] = None
    total_amount: Optional[DECIMAL] = None
    atpo_number: Optional[int] = None
    wrr_number: Optional[int] = None
    creation_tat: Optional[str] = None
    approver: Optional[str] = None
    date_approval: Optional[datetime] = None
    processing_tat: Optional[int] = None
    total_tat: Optional[int] = None
    approval_tat: Optional[int] = None
    remarks_return: Optional[str] = None
    channel: Optional[int] = None
    created_by: Optional[str] = None
    processed_by: Optional[str] = None


class SrFctHeaderCreate(SrFctHeaderBase):
    @field_validator("appkey")
    def validate_appkey(cls, v):
        if not v:
            raise ValueError("appkey cannot be empty")
        return v

    pass


class SrFctHeader(SrFctHeaderBase):
    """Base schema for SR header responses"""

    id: int


if TYPE_CHECKING:
    from .dimensions import DimCustomDropdown, DimCustomer
    from .sr_fct_items import SrFctItems
    from .sr_fct_attachment import SrFctAttachment
    from .sr_fct_logsremarksheader import SrFctLogsRemarksHeader


class SrFctHeaderComplete(SrFctHeader):
    """Complete schema including all relationships"""

    type_request: Optional["DimCustomDropdown"] = None
    reason_return: Optional["DimCustomDropdown"] = None
    mode_return: Optional["DimCustomDropdown"] = None
    status: Optional["DimCustomDropdown"] = None
    customer: Optional["DimCustomer"] = None
    items: List["SrFctItems"] = []
    header_logs: List["SrFctLogsRemarksHeader"] = []
    attachments: List["SrFctAttachment"] = []


class SrFctHeaderResponse(SrFctHeader):
    """Standard response schema for SR headers"""

    pass


class SrFctHeaderDetailResponse(SrFctHeaderComplete):
    """Detailed response schema with relationships"""

    pass


class SrFctHeaderListResponse(BaseSchema):
    """Paginated list response for SR headers"""

    items: List[SrFctHeader]
    total: int
    skip: int
    limit: int
