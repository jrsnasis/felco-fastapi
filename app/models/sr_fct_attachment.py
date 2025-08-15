from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class SrFctAttachment(Base):
    __tablename__ = "sr_fct_attachment"

    appkey = Column(String(20), ForeignKey("sr_fct_header.appkey"), primary_key=True)
    id = Column(Integer, unique=True, autoincrement=True)
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

    # Relationships
    header = relationship("SrFctHeader", back_populates="attachments")
