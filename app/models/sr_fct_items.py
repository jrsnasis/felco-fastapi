# app/models/sr_fct_items.py
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sr_fct_header import SrFctHeader
    from .dimensions import DimMara, DimCustomDropdown
    from .sr_fct_logsremarksitems import SrFctLogsRemarksItems


class SrFctItems(Base):
    __tablename__ = "sr_fct_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(255), nullable=False)  # Removed ForeignKey
    keyid = Column(String(255))
    matnr = Column(String(255))  # Removed ForeignKey
    fk_actiontype = Column(Integer)  # Removed ForeignKey
    discount = Column(DECIMAL(18, 2), nullable=False, default=0.00)
    qty = Column(Integer, nullable=False, default=0)
    srp = Column(DECIMAL(11, 2))
    total_amount = Column(DECIMAL(11, 2))
    net_price = Column(DECIMAL(11, 2))
    net_total_amount = Column(DECIMAL(11, 2))
    fsp_remarks = Column(String(255))
    ssa_remarks = Column(String(255))
    dr_number = Column(String(100))
    dr_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    m_created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    m_updated_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    code = Column(String(11))
    nsmemail = Column(String(225))
    gsmemail = Column(String(225))
    rsmemail = Column(String(225))
    fspemail = Column(String(225))
    is_sdo = Column(Integer)

    # Relationships (view-only foreign keys)
    header = relationship(
        "SrFctHeader",
        back_populates="items",
        primaryjoin="foreign(SrFctItems.appkey) == SrFctHeader.appkey",
        viewonly=True,
    )
    material = relationship(
        "DimMara",
        back_populates="sr_items",
        primaryjoin="foreign(SrFctItems.matnr) == DimMara.matnr",
        viewonly=True,
    )
    action_type = relationship(
        "DimCustomDropdown",
        back_populates="sr_items_action_type",
        primaryjoin="foreign(SrFctItems.fk_actiontype) == DimCustomDropdown.id",
        viewonly=True,
    )
    item_logs = relationship(
        "SrFctLogsRemarksItems",
        back_populates="item",
        primaryjoin="SrFctItems.appkey == foreign(SrFctLogsRemarksItems.appkey)",
        viewonly=True,
    )
