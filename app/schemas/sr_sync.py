# app/schemas/sr_sync.py
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from decimal import Decimal

from app.models.sr_fct_items import SrFctItems


class UserData(BaseModel):
    email: str
    code: str
    user_role: str  # "requestor", "validator", "approver", "unknown"


class SrSyncItemData(BaseModel):
    appkey: str
    keyid: str
    matnr: str
    fk_actiontype: int
    discount: Optional[Decimal] = None
    qty: int
    srp: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    net_price: Optional[Decimal] = None
    net_total_amount: Optional[Decimal] = None
    fsp_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    dr_number: Optional[str] = None
    dr_date: Optional[str] = None  # ISO format string
    code: str
    is_sdo: Optional[int] = None
    id: Optional[int] = None

    @classmethod
    def from_sr_item(cls, item: SrFctItems) -> "SrSyncItemData":
        """Convert SrFctItems model to SrSyncItemData"""
        return cls(
            appkey=item.appkey,
            keyid=item.keyid,
            matnr=item.matnr,
            fk_actiontype=item.fk_actiontype,
            discount=item.discount,
            qty=item.qty,
            srp=item.srp,
            total_amount=item.total_amount,
            net_price=item.net_price,
            net_total_amount=item.net_total_amount,
            fsp_remarks=item.fsp_remarks,
            ssa_remarks=item.ssa_remarks,
            dr_number=item.dr_number,
            dr_date=item.dr_date.isoformat() if item.dr_date else None,
            code=item.code,
            is_sdo=item.is_sdo,
            id=item.id,
        )


class SrSyncHeaderData(BaseModel):
    appkey: str
    keyid: str
    fk_typerequest: Optional[int] = None
    fk_reasonreturn: Optional[int] = None
    fk_modereturn: Optional[int] = None
    fk_status: Optional[int] = None
    fk_srrtype: Optional[int] = None
    code: str
    created_at: Optional[datetime] = None
    customer_code: str
    customer_name: str
    customer_address: str
    ship_name: str
    ship_to: str
    updated_shiptocode: str
    sdo_pao_remarks: Optional[str] = None
    ssa_remarks: Optional[str] = None
    approver_remarks: Optional[str] = None
    remarks_return: Optional[str] = None
    return_items: List[SrSyncItemData] = []
    replace_items: List[SrSyncItemData] = []


class SrSyncAttachmentData(BaseModel):
    appkey: str
    keyid: str
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    uploaded_at: Optional[str] = None  # ISO format string


class SrSyncResponse(BaseModel):
    user: UserData
    header: List[SrSyncHeaderData]
    attachments: List[SrSyncAttachmentData]

    class Config:
        from_attributes = True
