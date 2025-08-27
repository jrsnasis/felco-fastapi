from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    DECIMAL,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class SrFctHeader(Base):
    __tablename__ = "sr_fct_header"

    id = Column(Integer, primary_key=True, autoincrement=True)
    appkey = Column(String(255), nullable=False, unique=True)
    keyid = Column(String(255))

    # FKs → DimCustomDropdown
    fk_typerequest = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_reasonreturn = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_modereturn = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_status = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    channel = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    fk_srrtype = Column(Integer, ForeignKey("dim_custom_dropdown.id"))

    # Composite FK → DimCustomer
    kunnr = Column(String(10), nullable=False)
    code = Column(String(4), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            [kunnr, code], ["dim_customer.kunnr", "dim_customer.fspcode"]
        ),
    )

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
    # ssaemail = Column(String(100))  # Added for further ehancements
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
    created_by = Column(String(225))
    processed_by = Column(String(225))

    # Relationships
    type_request = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_typerequest],
        back_populates="sr_headers_type_request",
    )
    reason_return = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_reasonreturn],
        back_populates="sr_headers_reason_return",
    )
    mode_return = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_modereturn],
        back_populates="sr_headers_mode_return",
    )
    status = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_status],
        back_populates="sr_headers_status",
    )
    srr_type = relationship(
        "DimCustomDropdown",
        foreign_keys=[fk_srrtype],
        back_populates="sr_srr_type",
    )
    customer = relationship("DimCustomer", back_populates="headers")

    items = relationship("SrFctItems", back_populates="header")
    header_logs = relationship("SrFctLogsRemarksHeader", back_populates="header")
    attachments = relationship("SrFctAttachment", back_populates="header")
