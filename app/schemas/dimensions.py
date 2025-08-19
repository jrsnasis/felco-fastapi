# app/schemas/dimensions.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date
from typing import TYPE_CHECKING
from decimal import Decimal as DECIMAL


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SrDimTypeOfApprovalStatBase(BaseSchema):
    description: Optional[str] = None
    is_active: Optional[int] = None
    created_date: Optional[datetime] = None


class SrDimTypeOfApprovalStatCreate(SrDimTypeOfApprovalStatBase):
    pass


class SrDimTypeOfApprovalStat(SrDimTypeOfApprovalStatBase):
    id: int


class DimCustomDropdownBase(BaseSchema):
    name: str
    value: Optional[str] = None
    order_reason: Optional[str] = None
    description: Optional[str] = None
    module: Optional[str] = None
    for_integration: Optional[int] = 1
    active: Optional[str] = "1"
    for_sales_approval: Optional[int] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DimCustomDropdownCreate(DimCustomDropdownBase):
    pass


class DimCustomDropdown(DimCustomDropdownBase):
    id: int


class DimColorCodingBase(BaseSchema):
    colo: Optional[str] = None
    text1: Optional[str] = None
    module: Optional[str] = None


class DimColorCodingCreate(DimColorCodingBase):
    pass


class DimColorCoding(DimColorCodingBase):
    id: int


class DimCustomerBase(BaseSchema):
    fspcode: str
    kunnr: str
    name: Optional[str] = None
    address: Optional[str] = None
    fspemail: Optional[str] = None
    rsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    nsmemail: Optional[str] = None
    timestamp: Optional[datetime] = None
    updated: Optional[int] = None
    term: Optional[str] = None
    city: Optional[str] = None
    w_sales: Optional[int] = None
    w_sales_cycle: Optional[str] = None
    regio: Optional[str] = None
    bzirk: Optional[str] = None
    industry_code: Optional[str] = None
    sdo_grp: Optional[str] = None


class DimCustomerCreate(DimCustomerBase):
    pass


class DimCustomer(DimCustomerBase):
    id: Optional[int] = None


class DimDiscountBase(BaseSchema):
    kunnr: str
    matkl: str
    datbi: Optional[date] = None
    datab: Optional[date] = None
    kbetr: Optional[DECIMAL] = None
    updat: Optional[datetime] = None
    uptim: Optional[str] = None
    fspemail: Optional[str] = None
    rsmemail: Optional[str] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None


class DimDiscountCreate(DimDiscountBase):
    pass


class DimDiscount(DimDiscountBase):
    pass


class DimMaraBase(BaseSchema):
    matnr: str
    matkl: Optional[str] = None
    mvgr1: Optional[str] = None
    kbetr: Optional[DECIMAL] = None
    maktx: Optional[str] = None
    updat: Optional[str] = None
    uptim: Optional[str] = None
    desc_matgrp: Optional[str] = None
    desc_mvgr1: Optional[str] = None
    erdat: Optional[date] = None
    updat2: Optional[date] = None
    mstav: Optional[str] = None
    mstdv: Optional[date] = None
    unit: Optional[str] = None
    product_class: Optional[str] = None
    is_featured: Optional[int] = None
    PRDHA: Optional[str] = None
    b2b_dim_inventory_level_id: Optional[int] = None
    exclusive: Optional[int] = None


class DimMaraCreate(DimMaraBase):
    pass


class DimMara(DimMaraBase):
    pass


if TYPE_CHECKING:
    from models.fct_visits import FctVisits
    from models.sr_fct_header import SrFctHeader
    from models.sr_fct_items import SrFctItems
    from models.sr_fct_logsremarksheader import SrFctLogsRemarksHeader
    from models.sr_fct_logsremarksitems import SrFctLogsRemarksItems


class DimCustomerComplete(DimCustomer):
    visits: List["FctVisits"] = []
    sr_headers: List["SrFctHeader"] = []


class DimMaraComplete(DimMara):
    sr_items: List["SrFctItems"] = []
    discounts: List[DimDiscount] = []


class DimCustomDropdownComplete(DimCustomDropdown):
    sr_headers_type_request: List["SrFctHeader"] = []
    sr_headers_reason_return: List["SrFctHeader"] = []
    sr_headers_mode_return: List["SrFctHeader"] = []
    sr_headers_status: List["SrFctHeader"] = []
    sr_items_action_type: List["SrFctItems"] = []


class SrDimTypeOfApprovalStatComplete(SrDimTypeOfApprovalStat):
    header_logs: List["SrFctLogsRemarksHeader"] = []
    item_logs: List["SrFctLogsRemarksItems"] = []
