# app/schemas/sr_fct_header.py
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class SrFctHeaderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    return_total: Optional[Decimal] = None
    replacement_total: Optional[Decimal] = None
    nsmemail: Optional[str] = None
    gsmemail: Optional[str] = None
    rsmemail: Optional[str] = None
    fspemail: Optional[str] = None
    code: Optional[str] = None
    date_submitted_ssa: Optional[datetime] = None
    date_sent_approval: Optional[datetime] = None
    fsp: Optional[str] = None
    rsm: Optional[str] = None
    total_amount: Optional[Decimal] = None
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
    @classmethod
    def validate_appkey(cls, v):
        if not v or not v.strip():
            raise ValueError("appkey cannot be empty")
        return v.strip()


class SrFctHeaderUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Only include fields that can be updated
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
    return_total: Optional[Decimal] = None
    replacement_total: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    date_approval: Optional[datetime] = None
    approver: Optional[str] = None
    remarks_return: Optional[str] = None
    processed_by: Optional[str] = None


class SrFctHeaderResponse(SrFctHeaderBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SrFctHeaderListResponse(BaseModel):
    items: List[SrFctHeaderResponse]
    total: int
    skip: int
    limit: int
