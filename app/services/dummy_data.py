# app/services/dummy_data.py
from datetime import datetime, date, time
from decimal import Decimal
from typing import List
import uuid
import random

from app.schemas.fct_visits import FctVisitsCreate
from app.schemas.sr_fct_header import SrFctHeaderCreate
from app.schemas.sr_fct_items import SrFctItemsCreate


class DummyDataService:
    """Service for generating dummy data for testing and development"""

    @staticmethod
    def generate_visits_dummy_data(count: int = 5) -> List[FctVisitsCreate]:
        """Generate dummy visit data"""
        visits = []

        # Sample data
        customers = [
            ("CUST001", "ABC Corporation", "123 Business St, Makati City"),
            ("CUST002", "XYZ Trading", "456 Commerce Ave, BGC, Taguig"),
            ("CUST003", "DEF Enterprises", "789 Industry Blvd, Pasig City"),
            ("CUST004", "GHI Solutions", "321 Tech Park, Ortigas Center"),
            ("CUST005", "JKL Distribution", "654 Warehouse St, Marikina City"),
        ]

        codes = ["FSP1", "FSP2", "FSP3", "FSP4"]
        vtypes = ["SALES", "COLLECTION", "DELIVERY", "SERVICE"]

        for i in range(count):
            customer = random.choice(customers)
            code = random.choice(codes)
            vtype = random.choice(vtypes)

            # Generate unique appkey
            appkey = (
                f"VIS{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
            )

            visit = FctVisitsCreate(
                appkey=appkey,
                empid=random.randint(1001, 1010),
                nsmemail=f"nsm{random.randint(1, 5)}@company.com",
                gsmemail=f"gsm{random.randint(1, 5)}@company.com",
                rsmemail=f"rsm{random.randint(1, 5)}@company.com",
                fspemail=f"fsp{random.randint(1, 5)}@company.com",
                code=code,
                vdate=date.today(),
                kunnr=customer[0],
                name=customer[1],
                address=customer[2],
                map=f"Map link for {customer[1]}",
                kmr=f"KMR{random.randint(100, 999)}",
                t1=time(8, random.randint(0, 59)),
                t2=time(17, random.randint(0, 59)),
                expense=Decimal(str(random.uniform(500, 2000))),
                sales=Decimal(str(random.uniform(10000, 50000))),
                remarks=f"Visit completed successfully for {customer[1]}",
                vtype=vtype,
                latlong=f"{random.uniform(14.4, 14.8)},{random.uniform(120.9, 121.2)}",
                timestamp=datetime.now(),
                creationdate=datetime.now(),
                updatedate=datetime.now(),
                tags=f"customer,{vtype.lower()},active",
                sales_target=Decimal(str(random.uniform(20000, 100000))),
                collection_target=Decimal(str(random.uniform(15000, 80000))),
                frequency="WEEKLY",
                imei=f"86{random.randint(1000000000000, 9999999999999)}",
                created_at=datetime.now(),
                work_type="REGULAR",
                customer_business_relationship="DISTRIBUTOR",
                is_unified=1,
            )
            visits.append(visit)

        return visits

    @staticmethod
    def generate_sr_header_dummy_data(
        visit_appkeys: List[str], count: int = 3
    ) -> List[SrFctHeaderCreate]:
        """Generate dummy SR header data using visit appkeys"""
        sr_headers = []

        # Sample data
        customers = [
            ("CUST001", "ABC Corporation"),
            ("CUST002", "XYZ Trading"),
            ("CUST003", "DEF Enterprises"),
            ("CUST004", "GHI Solutions"),
            ("CUST005", "JKL Distribution"),
        ]

        codes = ["FSP1", "FSP2", "FSP3", "FSP4"]
        reasons = ["DAMAGED", "EXPIRED", "WRONG_ITEM", "QUALITY_ISSUE"]

        for i in range(min(count, len(visit_appkeys))):
            customer = random.choice(customers)
            code = random.choice(codes)
            reason = random.choice(reasons)

            # Use visit appkey or generate new one
            appkey = (
                visit_appkeys[i]
                if i < len(visit_appkeys)
                else f"SR{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4())[:8].upper()}"
            )

            sr_header = SrFctHeaderCreate(
                appkey=appkey,
                keyid=f"KEY{random.randint(10000, 99999)}",
                fk_typerequest=random.randint(
                    1, 3
                ),  # Assuming dropdown IDs 1-3 for type
                fk_reasonreturn=random.randint(
                    4, 7
                ),  # Assuming dropdown IDs 4-7 for reason
                fk_modereturn=random.randint(
                    8, 10
                ),  # Assuming dropdown IDs 8-10 for mode
                fk_status=random.randint(
                    11, 15
                ),  # Assuming dropdown IDs 11-15 for status
                kunnr=customer[0],
                updated_shiptocode=f"ST{random.randint(100, 999)}",
                ship_name=customer[1],
                ship_to=f"Ship to address for {customer[1]}",
                sdo_pao_remarks=f"SDO/PAO remarks for {reason}",
                ssa_remarks=f"SSA review completed for {customer[1]}",
                approver_remarks="Approved for processing",
                return_total=Decimal(str(random.uniform(5000, 25000))),
                replacement_total=Decimal(str(random.uniform(3000, 20000))),
                nsmemail=f"nsm{random.randint(1, 5)}@company.com",
                gsmemail=f"gsm{random.randint(1, 5)}@company.com",
                rsmemail=f"rsm{random.randint(1, 5)}@company.com",
                fspemail=f"fsp{random.randint(1, 5)}@company.com",
                code=code,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                m_created_at=datetime.now(),
                m_updated_at=datetime.now(),
                fsp=f"FSP {random.randint(1, 10)}",
                rsm=f"RSM {random.randint(1, 5)}",
                total_amount=Decimal(str(random.uniform(8000, 45000))),
                atpo_number=random.randint(100000, 999999),
                wrr_number=random.randint(200000, 899999),
                creation_tat=f"{random.randint(1, 48)} hours",
                approver=f"Approver {random.randint(1, 5)}",
                processing_tat=random.randint(24, 120),
                total_tat=random.randint(48, 168),
                approval_tat=random.randint(12, 72),
                remarks_return=f"Return processed for {reason}",
                channel=random.randint(1, 3),
                created_by=f"user{random.randint(1, 10)}@company.com",
                processed_by=f"processor{random.randint(1, 5)}@company.com",
            )
            sr_headers.append(sr_header)

        return sr_headers

    @staticmethod
    def generate_sr_items_dummy_data(
        sr_appkeys: List[str], items_per_header: int = 2
    ) -> List[SrFctItemsCreate]:
        """Generate dummy SR items data for given SR headers"""
        sr_items = []

        # Sample materials
        materials = [
            ("MAT001", Decimal("1250.00"), "Product A"),
            ("MAT002", Decimal("2100.50"), "Product B"),
            ("MAT003", Decimal("850.75"), "Product C"),
            ("MAT004", Decimal("3200.00"), "Product D"),
            ("MAT005", Decimal("950.25"), "Product E"),
        ]

        codes = ["FSP1", "FSP2", "FSP3", "FSP4"]

        for appkey in sr_appkeys:
            for i in range(items_per_header):
                material = random.choice(materials)
                code = random.choice(codes)
                qty = random.randint(1, 10)
                discount = Decimal(str(random.uniform(0, 15)))  # 0-15% discount

                # Calculate amounts
                srp = material[1]
                gross_total = srp * qty
                # discount_amount = gross_total * (discount / 100)
                net_price = srp - (srp * discount / 100)
                net_total_amount = net_price * qty

                sr_item = SrFctItemsCreate(
                    appkey=appkey,
                    keyid=f"ITEM{random.randint(10000, 99999)}",
                    matnr=material[0],
                    fk_actiontype=random.randint(
                        16, 20
                    ),  # Assuming dropdown IDs 16-20 for action type
                    discount=discount,
                    qty=qty,
                    srp=srp,
                    total_amount=gross_total,
                    net_price=net_price,
                    net_total_amount=net_total_amount,
                    fsp_remarks=f"FSP remarks for {material[2]}",
                    ssa_remarks=f"SSA reviewed {material[2]} - {qty} pcs",
                    dr_number=f"DR{random.randint(100000, 999999)}",
                    dr_date=datetime.now(),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    m_created_at=datetime.now(),
                    m_updated_at=datetime.now(),
                    code=code,
                    nsmemail=f"nsm{random.randint(1, 5)}@company.com",
                    gsmemail=f"gsm{random.randint(1, 5)}@company.com",
                    rsmemail=f"rsm{random.randint(1, 5)}@company.com",
                    fspemail=f"fsp{random.randint(1, 5)}@company.com",
                    is_sdo=random.randint(0, 1),
                )
                sr_items.append(sr_item)

        return sr_items

    @staticmethod
    def create_complete_dummy_dataset(
        visit_count: int = 5, sr_header_count: int = 3, items_per_header: int = 2
    ) -> dict:
        """Create a complete dummy dataset with visits, SR headers, and items"""

        # Generate visits
        visits = DummyDataService.generate_visits_dummy_data(visit_count)
        visit_appkeys = [visit.appkey for visit in visits]

        # Generate SR headers using some visit appkeys
        sr_headers = DummyDataService.generate_sr_header_dummy_data(
            visit_appkeys, sr_header_count
        )
        sr_appkeys = [header.appkey for header in sr_headers]

        # Generate SR items
        sr_items = DummyDataService.generate_sr_items_dummy_data(
            sr_appkeys, items_per_header
        )

        return {
            "visits": visits,
            "sr_headers": sr_headers,
            "sr_items": sr_items,
            "visit_appkeys": visit_appkeys,
            "sr_appkeys": sr_appkeys,
        }


# Create instance for easy importing
dummy_data_service = DummyDataService()
