from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class SrFctLogsRemarksHeader(Base):
    __tablename__ = "sr_fct_logsremarksheader"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(50))
    keyid = Column(String(50), ForeignKey("sr_fct_header.keyid"), nullable=False)
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
    header = relationship("SrFctHeader", back_populates="header_logs")
    approval_status = relationship(
        "SrDimTypeOfApprovalStat", back_populates="header_logs"
    )
