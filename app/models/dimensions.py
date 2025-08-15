from sqlalchemy import Column, Integer, String, DateTime, Date, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class SrDimTypeOfApprovalStat(Base):
    __tablename__ = "sr_dim_typeofapprovalstat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Integer)
    created_date = Column(DateTime)
    description = Column(String(255))

    # Relationships
    header_logs = relationship(
        "SrFctLogsRemarksHeader", back_populates="approval_status"
    )
    item_logs = relationship("SrFctLogsRemarksItems", back_populates="approval_status")


class DimCustomDropdown(Base):
    __tablename__ = "dim_custom_dropdown"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    value = Column(String(255))
    order_reason = Column(String(100), comment="order reason based on po supplement")
    description = Column(String(255))
    module = Column(String(255))
    for_integration = Column(Integer, default=1, comment="1 = include integration")
    active = Column(String(255), default="1")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)
    for_sales_approval = Column(Integer)
    tags = Column(String(50))
    category = Column(String(255))
    subcategory = Column(String(255))
    created_by = Column(String(255))
    updated_by = Column(String(255))

    # Relationships based on different dropdown types
    sr_headers_type_request = relationship(
        "SrFctHeader",
        foreign_keys="SrFctHeader.fk_typerequest",
        back_populates="type_request",
    )
    sr_headers_reason_return = relationship(
        "SrFctHeader",
        foreign_keys="SrFctHeader.fk_reasonreturn",
        back_populates="reason_return",
    )
    sr_headers_mode_return = relationship(
        "SrFctHeader",
        foreign_keys="SrFctHeader.fk_modereturn",
        back_populates="mode_return",
    )
    sr_headers_status = relationship(
        "SrFctHeader", foreign_keys="SrFctHeader.fk_status", back_populates="status"
    )
    sr_items_action_type = relationship("SrFctItems", back_populates="action_type")


class DimColorCoding(Base):
    __tablename__ = "dim_color_coding"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colo = Column(String(20))
    text1 = Column(String(20))
    module = Column(String(20))


class DimCustomer(Base):
    __tablename__ = "dim_customer"

    id = Column(Integer)
    fspcode = Column(String(4), primary_key=True)
    kunnr = Column(String(10), primary_key=True)
    name = Column(String(150))
    address = Column(String(150))
    fspemail = Column(String(300))
    rsmemail = Column(String(300))
    gsmemail = Column(String(300))
    nsmemail = Column(String(300))
    timestamp = Column(DateTime)
    updated = Column(Integer)
    term = Column(String(6))
    city = Column(String(40))
    w_sales = Column(Integer)
    w_sales_cycle = Column(String(10))
    regio = Column(String(50))
    bzirk = Column(String(50))
    industry_code = Column(String(4))
    sdo_grp = Column(String(2))

    # Relationships
    visits = relationship("FctVisits", back_populates="customer")
    sr_headers = relationship("SrFctHeader", back_populates="customer")


class DimDiscount(Base):
    __tablename__ = "dim_discount"

    kunnr = Column(String(10), primary_key=True)
    matkl = Column(String(9), primary_key=True)
    datbi = Column(Date)
    datab = Column(Date)
    kbetr = Column(DECIMAL(18, 2))
    updat = Column(DateTime)
    uptim = Column(String(11))
    fspemail = Column(String(999))
    rsmemail = Column(String(999))
    nsmemail = Column(String(999))
    gsmemail = Column(String(999))

    # Relationships
    customer = relationship(
        "DimCustomer", primaryjoin="and_(DimDiscount.kunnr == DimCustomer.kunnr)"
    )
    material = relationship("DimMara", primaryjoin="DimDiscount.matkl == DimMara.matkl")


class DimMara(Base):
    __tablename__ = "dim_mara"

    matnr = Column(String(18), primary_key=True)
    matkl = Column(String(9))
    mvgr1 = Column(String(3))
    kbetr = Column(DECIMAL(18, 3))
    maktx = Column(String(150))
    updat = Column(String(50))
    uptim = Column(String(50))
    desc_matgrp = Column(String(255))
    desc_mvgr1 = Column(String(255))
    erdat = Column(Date)
    updat2 = Column(Date)
    mstav = Column(String(255))
    mstdv = Column(Date)
    unit = Column(String(50))
    product_class = Column(String(1))
    is_featured = Column(Integer)
    PRDHA = Column(String(18))
    b2b_dim_inventory_level_id = Column(Integer)
    exclusive = Column(Integer)

    # Relationships
    sr_items = relationship("SrFctItems", back_populates="material")
    discounts = relationship(
        "DimDiscount", primaryjoin="DimMara.matkl == DimDiscount.matkl"
    )
