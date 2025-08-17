# app/schemas/fct_visits.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date, time
from typing import TYPE_CHECKING
from decimal import Decimal as DECIMAL


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FctVisitsBase(BaseSchema):
    appkey: str
    empid: Optional[int] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    rsmemail: Optional[str] = None
    fspemail: Optional[str] = None
    code: Optional[str] = None
    vdate: date
    kunnr: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    map: Optional[str] = None
    kmr: Optional[str] = None
    t1: Optional[time] = None
    t2: Optional[time] = None
    expense: Optional[DECIMAL] = None
    sales: Optional[DECIMAL] = None
    remarks: Optional[str] = None
    vtype: Optional[str] = None
    latlong: Optional[str] = None
    timestamp: Optional[datetime] = None
    cp_remarks: Optional[str] = None
    creationdate: Optional[datetime] = None
    updatedate: Optional[datetime] = None
    audit_amt: Optional[DECIMAL] = None
    audit_date: Optional[str] = None
    audit_remarks: Optional[str] = None
    n1: Optional[DECIMAL] = None
    n2: Optional[DECIMAL] = None
    d1: Optional[datetime] = None
    d2: Optional[datetime] = None
    text1: Optional[str] = None
    text2: Optional[str] = None
    audcrtdate: Optional[datetime] = None
    auditemail: Optional[str] = None
    so_number: Optional[str] = None
    tlm_remarks: Optional[str] = None
    tlm_crtdate: Optional[datetime] = None
    tlm_updatedate: Optional[datetime] = None
    tlm_email: Optional[str] = None
    auduptdate: Optional[datetime] = None
    md: Optional[datetime] = None
    t2_copy: Optional[time] = None
    ship_to_party: Optional[str] = None
    po_num: Optional[str] = None
    po_date: Optional[date] = None
    version: Optional[str] = None
    po_num_supp: Optional[str] = None
    header_note2: Optional[str] = None
    order_item_count: Optional[int] = None
    ftp_so_uploaded_at: Optional[datetime] = None
    ftp_so_error_at: Optional[datetime] = None
    ftp_so_error_message: Optional[str] = None
    is_final: Optional[str] = None
    date_final: Optional[datetime] = None
    date_final_synced: Optional[datetime] = None
    so_xml_doc_id: Optional[int] = None
    so_error_id: Optional[int] = None
    order_type: Optional[str] = "ZOR"
    booking_status_id: Optional[int] = None
    booking_status_id2: Optional[int] = None
    manual_setup_at: Optional[datetime] = None
    integration_status: Optional[int] = 0
    integration_status_created_at: Optional[datetime] = None
    integration_status_updated_at: Optional[datetime] = None
    integration_so_numbers: Optional[str] = None
    tags: Optional[str] = None
    sales_target: Optional[DECIMAL] = None
    collection_target: Optional[DECIMAL] = None
    frequency: Optional[str] = None

    # Image fields
    img1: Optional[str] = None
    img2: Optional[str] = None
    img3: Optional[str] = None
    img4: Optional[str] = None
    img5: Optional[str] = None
    img6: Optional[str] = None
    img7: Optional[str] = None
    img8: Optional[str] = None
    img9: Optional[str] = None
    img10: Optional[str] = None

    # Image creation/update dates
    img1_creationdate: Optional[datetime] = None
    img1_updatedate: Optional[datetime] = None
    img2_creationdate: Optional[datetime] = None
    img2_updatedate: Optional[datetime] = None
    img3_creationdate: Optional[datetime] = None
    img3_updatedate: Optional[datetime] = None
    img4_creationdate: Optional[datetime] = None
    img4_updatedate: Optional[datetime] = None
    img5_creationdate: Optional[datetime] = None
    img5_updatedate: Optional[datetime] = None
    img6_creationdate: Optional[datetime] = None
    img6_updatedate: Optional[datetime] = None
    img7_creationdate: Optional[datetime] = None
    img7_updatedate: Optional[datetime] = None
    img8_creationdate: Optional[datetime] = None
    img8_updatedate: Optional[datetime] = None
    img9_creationdate: Optional[datetime] = None
    img9_updatedate: Optional[datetime] = None
    img10_creationdate: Optional[datetime] = None
    img10_updatedate: Optional[datetime] = None

    # Additional fields
    with_po: Optional[int] = None
    imei: Optional[str] = None
    created_at: Optional[datetime] = None
    work_type: Optional[str] = None
    mcp_updated_at: Optional[datetime] = None
    mcp_upload_created_at: Optional[datetime] = None
    customer_business_relationship: Optional[str] = None
    is_unified: Optional[int] = None
    so_date: Optional[str] = None
    unified_integration_read_at: Optional[datetime] = None
    unified_integration_so_number: Optional[str] = None
    unified_integration_so_date: Optional[str] = None
    unified_integration_finished_at: Optional[datetime] = None
    unified_integration_transfered_at: Optional[datetime] = None
    unified_integration_retry_at: Optional[datetime] = None
    latlong_timeout: Optional[str] = None


class FctVisitsCreate(FctVisitsBase):
    """Schema for creating new visit records"""

    pass


class FctVisits(FctVisitsBase):
    """Base schema for visit responses"""

    pass


if TYPE_CHECKING:
    from .dimensions import DimCustomer


class FctVisitsComplete(FctVisits):
    """Complete schema including customer relationship"""

    customer: Optional["DimCustomer"] = None


class FctVisitsResponse(FctVisits):
    """Standard response schema for visits"""

    pass


class FctVisitsListResponse(BaseSchema):
    """Paginated list response for visits"""

    items: list[FctVisits]
    total: int
    skip: int
    limit: int
