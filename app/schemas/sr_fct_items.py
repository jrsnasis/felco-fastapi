# app/schemas/sr_fct_items.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal as DECIMAL


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


class SrFctItemsUpdate(BaseSchema):
    """Schema for updating SR item records"""
    appkey: Optional[str] = None
    keyid: Optional[str] = None
    matnr: Optional[str] = None
    fk_actiontype: Optional[int] = None
    discount: Optional[DECIMAL] = None
    qty: Optional[int] = None
    srp: Optional[DECIMAL] = None
    total_amount: Optional[DECIMAL] = None
    net_price: Optional[DECIMAL] = None
    net_total_amount: Optional[DECIMAL] = None
    fsp_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    dr_number: Optional[str] = None
    dr_date: Optional[datetime] = None
    code: Optional[str] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    rsmemail: Optional[str] = None
    fspemail: Optional[str] = None
    is_sdo: Optional[int] = None


class SrFctItemsResponse(SrFctItemsBase):
    """Base schema for SR item responses"""
    id: int
    created_at: datetime
    updated_at: datetime
    m_created_at: datetime
    m_updated_at: datetime


class SrFctItemsListResponse(BaseSchema):
    """Paginated list response for SR items"""
    items: List[SrFctItemsResponse]
    total: int
    skip: int
    limit: int
