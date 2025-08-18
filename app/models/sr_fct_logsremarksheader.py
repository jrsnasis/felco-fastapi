# app/models/sr_fct_logsremarksheader.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sr_fct_header import SrFctHeader
    from .dimensions import SrDimTypeOfApprovalStat


class SrFctLogsRemarksHeader(Base):
    __tablename__ = "sr_fct_logsremarksheader"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(50), nullable=False)  # Removed ForeignKey
    keyid = Column(String(50))
    fk_typeapprovalstatus = Column(Integer)  # Removed ForeignKey
    remarks = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    type_remarks = Column(String(255))
    created_by = Column(String(225))

    # Relationships (view-only foreign keys)
    header = relationship(
        "SrFctHeader",
        back_populates="header_logs",
        primaryjoin="foreign(SrFctLogsRemarksHeader.appkey) == SrFctHeader.appkey",
        viewonly=True,
    )
    approval_status = relationship(
        "SrDimTypeOfApprovalStat",
        back_populates="header_logs",
        primaryjoin="foreign(SrFctLogsRemarksHeader.fk_typeapprovalstatus) == SrDimTypeOfApprovalStat.id",
        viewonly=True,
    )
