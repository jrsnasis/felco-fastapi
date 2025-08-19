from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sr_fct_items import SrFctItems
    from .dimensions import SrDimTypeOfApprovalStat


class SrFctLogsRemarksItems(Base):
    __tablename__ = "sr_fct_logsremarksitems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(50), ForeignKey("sr_fct_items.appkey"), nullable=False)
    keyid = Column(String(50))
    fk_typeapprovalstatus = Column(Integer, ForeignKey("sr_dim_typeofapprovalstat.id"))
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

    # Relationships
    item = relationship("SrFctItems", back_populates="item_logs")
    approval_status = relationship(
        "SrDimTypeOfApprovalStat", back_populates="item_logs"
    )
