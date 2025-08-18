# app/models/sr_fct_header.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dimensions import DimCustomDropdown, DimCustomer
    from .sr_fct_items import SrFctItems
    from .sr_fct_attachment import SrFctAttachment
    from .sr_fct_logsremarksheader import SrFctLogsRemarksHeader


class SrFctHeader(Base):
    __tablename__ = "sr_fct_header"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(255), nullable=False, unique=True)
    keyid = Column(String(255))
    fk_typerequest = Column(Integer)  # Removed ForeignKey
    fk_reasonreturn = Column(Integer)  # Removed ForeignKey
    fk_modereturn = Column(Integer)  # Removed ForeignKey
    fk_status = Column(Integer)  # Removed ForeignKey
    kunnr = Column(String(10))
    updated_shiptocode = Column(String(10))
    ship_name = Column(String(225))
    ship_to = Column(String(225))
    sdo_pao_remarks = Column(String(225))
    ssa_remarks = Column(String(225))
    approver_remarks = Column(String(225))
    return_total = Column(DECIMAL(18, 2))
    replacement_total = Column(DECIMAL(18, 2))
    nsmemail = Column(String(50))
    gsmemail = Column(String(50))
    rsmemail = Column(String(50))
    fspemail = Column(String(50))
    code = Column(String(4))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_submitted_ssa = Column(DateTime)
    date_sent_approval = Column(DateTime)
    fsp = Column(String(225))
    rsm = Column(String(225))
    total_amount = Column(DECIMAL(18, 2))
    atpo_number = Column(Integer)
    wrr_number = Column(Integer)
    creation_tat = Column(String(225))
    approver = Column(String(225))
    date_approval = Column(DateTime)
    processing_tat = Column(Integer)
    total_tat = Column(Integer)
    approval_tat = Column(Integer)
    remarks_return = Column(String(225))
    channel = Column(Integer)
    created_by = Column(String(225))
    processed_by = Column(String(225))

    # Relationships (view-only foreign keys)
    type_request = relationship(
        "DimCustomDropdown",
        back_populates="sr_headers_type_request",
        primaryjoin="foreign(SrFctHeader.fk_typerequest) == DimCustomDropdown.id",
        viewonly=True,
    )
    reason_return = relationship(
        "DimCustomDropdown",
        back_populates="sr_headers_reason_return",
        primaryjoin="foreign(SrFctHeader.fk_reasonreturn) == DimCustomDropdown.id",
        viewonly=True,
    )
    mode_return = relationship(
        "DimCustomDropdown",
        back_populates="sr_headers_mode_return",
        primaryjoin="foreign(SrFctHeader.fk_modereturn) == DimCustomDropdown.id",
        viewonly=True,
    )
    status = relationship(
        "DimCustomDropdown",
        back_populates="sr_headers_status",
        primaryjoin="foreign(SrFctHeader.fk_status) == DimCustomDropdown.id",
        viewonly=True,
    )
    customer = relationship(
        "DimCustomer",
        back_populates="headers",
        primaryjoin="and_(foreign(SrFctHeader.kunnr) == DimCustomer.kunnr, foreign(SrFctHeader.code) == DimCustomer.fspcode)",
        viewonly=True,
    )
    items = relationship(
        "SrFctItems",
        back_populates="header",
        primaryjoin="SrFctHeader.appkey == foreign(SrFctItems.appkey)",
        viewonly=True,
    )
    header_logs = relationship(
        "SrFctLogsRemarksHeader",
        back_populates="header",
        primaryjoin="SrFctHeader.appkey == foreign(SrFctLogsRemarksHeader.appkey)",
        viewonly=True,
    )
    attachments = relationship(
        "SrFctAttachment",
        back_populates="header",
        primaryjoin="SrFctHeader.appkey == foreign(SrFctAttachment.appkey)",
        viewonly=True,
    )
