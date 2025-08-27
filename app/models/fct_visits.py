from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Text,
    Time,
    DECIMAL,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base


class FctVisits(Base):
    __tablename__ = "fct_visits"

    appkey = Column(String(50), primary_key=True)
    empid = Column(Integer)
    nsmemail = Column(String(50))
    gsmemail = Column(String(50))
    rsmemail = Column(String(50))
    fspemail = Column(String(50))
    code = Column(String(10), nullable=False)
    kunnr = Column(String(10), nullable=False)

    # FK → DimCustomer
    __table_args__ = (
        ForeignKeyConstraint(
            [kunnr, code], ["dim_customer.kunnr", "dim_customer.fspcode"]
        ),
    )

    vdate = Column(Date, nullable=False)
    name = Column(String(150))
    address = Column(String(150))
    map = Column(String(150))
    kmr = Column(String(50))
    t1 = Column(Time)
    t2 = Column(Time)
    expense = Column(DECIMAL(10, 2))
    sales = Column(DECIMAL(10, 2))
    remarks = Column(String(150))
    vtype = Column(String(10))
    latlong = Column(String(50))
    timestamp = Column(DateTime)
    cp_remarks = Column(String(150))
    creationdate = Column(DateTime)
    updatedate = Column(DateTime)
    audit_amt = Column(DECIMAL(10, 2))
    audit_date = Column(String(150))
    audit_remarks = Column(String(150))
    n1 = Column(DECIMAL(10, 2))
    n2 = Column(DECIMAL(10, 2))
    d1 = Column(DateTime)
    d2 = Column(DateTime)
    text1 = Column(String(150))
    text2 = Column(String(150))
    audcrtdate = Column(DateTime)
    auditemail = Column(String(255))
    so_number = Column(String(255))
    tlm_remarks = Column(String(1000))
    tlm_crtdate = Column(DateTime)
    tlm_updatedate = Column(DateTime)
    tlm_email = Column(String(50))
    auduptdate = Column(DateTime)
    md = Column(DateTime)
    t2_copy = Column(Time)
    ship_to_party = Column(String(255))
    po_num = Column(String(255))
    po_date = Column(Date)
    version = Column(String(255))
    po_num_supp = Column(String(255))
    header_note2 = Column(String(500))
    order_item_count = Column(Integer)
    ftp_so_uploaded_at = Column(DateTime)
    ftp_so_error_at = Column(DateTime)
    ftp_so_error_message = Column(String(255))
    is_final = Column(String(255))
    date_final = Column(DateTime)
    date_final_synced = Column(DateTime)
    so_xml_doc_id = Column(Integer)
    so_error_id = Column(Integer)
    order_type = Column(String(10), default="ZOR")

    # FKs → DimCustomDropdown
    booking_status_id = Column(Integer, ForeignKey("dim_custom_dropdown.id"))
    booking_status_id2 = Column(Integer, ForeignKey("dim_custom_dropdown.id"))

    manual_setup_at = Column(DateTime)
    integration_status = Column(Integer, default=0)
    integration_status_created_at = Column(DateTime)
    integration_status_updated_at = Column(DateTime)
    integration_so_numbers = Column(String(500))
    tags = Column(String(150))
    sales_target = Column(DECIMAL(16, 2))
    collection_target = Column(DECIMAL(16, 2))
    frequency = Column(String(10))

    # Image fields
    img1 = Column(String(500))
    img2 = Column(String(500))
    img3 = Column(String(500))
    img4 = Column(String(500))
    img5 = Column(String(500))
    img6 = Column(String(500))
    img7 = Column(String(500))
    img8 = Column(String(500))
    img9 = Column(String(500))
    img10 = Column(String(500))

    # Image creation/update dates
    img1_creationdate = Column(DateTime)
    img1_updatedate = Column(DateTime)
    img2_creationdate = Column(DateTime)
    img2_updatedate = Column(DateTime)
    img3_creationdate = Column(DateTime)
    img3_updatedate = Column(DateTime)
    img4_creationdate = Column(DateTime)
    img4_updatedate = Column(DateTime)
    img5_creationdate = Column(DateTime)
    img5_updatedate = Column(DateTime)
    img6_creationdate = Column(DateTime)
    img6_updatedate = Column(DateTime)
    img7_creationdate = Column(DateTime)
    img7_updatedate = Column(DateTime)
    img8_creationdate = Column(DateTime)
    img8_updatedate = Column(DateTime)
    img9_creationdate = Column(DateTime)
    img9_updatedate = Column(DateTime)
    img10_creationdate = Column(DateTime)
    img10_updatedate = Column(DateTime)

    with_po = Column(Integer)
    imei = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    work_type = Column(String(255))
    mcp_updated_at = Column(DateTime)
    mcp_upload_created_at = Column(
        DateTime, comment="tagging if from web upload or mobile"
    )
    customer_business_relationship = Column(String(150))
    is_unified = Column(Integer)
    so_date = Column(Text)
    unified_integration_read_at = Column(DateTime)
    unified_integration_so_number = Column(Text)
    unified_integration_so_date = Column(Text)
    unified_integration_finished_at = Column(DateTime)
    unified_integration_transfered_at = Column(DateTime)
    unified_integration_retry_at = Column(DateTime)
    latlong_timeout = Column(String(50))

    # Relationships
    customer = relationship(
        "DimCustomer",
        back_populates="visits",
    )

    booking_status = relationship("DimCustomDropdown", foreign_keys=[booking_status_id])
    booking_status2 = relationship(
        "DimCustomDropdown", foreign_keys=[booking_status_id2]
    )
