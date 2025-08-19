from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sr_fct_header import SrFctHeader


class SrFctAttachment(Base):
    __tablename__ = "sr_fct_attachment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(20), ForeignKey("sr_fct_header.appkey"), nullable=False)
    keyid = Column(String(20))
    image = Column(String(255))
    image_tag = Column(String(50))
    is_active = Column(Boolean)
    table_name = Column(String(255))
    file_name = Column(String(225))
    file_path = Column(String(225))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    m_created_at = Column(DateTime)
    m_updated_at = Column(DateTime)
    upload_state = Column(Integer)
    uploaded_by = Column(String(255))

    # Relationship
    header = relationship("SrFctHeader", back_populates="attachments")
