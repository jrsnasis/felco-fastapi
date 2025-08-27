# app/crud/sr_sync.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Dict, List, Optional
import logging

from app.models.sr_fct_header import SrFctHeader
from app.models.sr_fct_items import SrFctItems
from app.models.sr_fct_attachment import SrFctAttachment
from app.models.fct_visits import FctVisits
from app.schemas.sr_sync import SrSyncHeaderData, SrSyncItemData, UserData

logger = logging.getLogger(__name__)


class CRUDSrSync:
    def __init__(self):
        pass

    def _get_user_role(self, email: str, header: SrFctHeader) -> str:
        """Determine user role based on email matching (without ssaemail for now)"""
        if email == header.fspemail:
            return "requestor"
        elif email == header.rsmemail:
            return "validator"
        # Note: ssaemail removed for now - will be added in further enhancements
        else:
            return "unknown"

    def get_sr_data_by_email(
        self, db: Session, *, email: str, keyid: Optional[str] = None
    ) -> Dict:
        """Get all SR data structured according to the required JSON format"""

        # Base query for headers - removed ssaemail for now
        header_query = db.query(SrFctHeader).filter(
            or_(
                SrFctHeader.fspemail == email,
                SrFctHeader.rsmemail == email,
                # SrFctHeader.ssaemail == email  # Removed for now - future enhancement
            )
        )

        # Add keyid filter if provided
        if keyid:
            header_query = header_query.filter(SrFctHeader.keyid == keyid)

        headers = header_query.all()

        if not headers:
            return {
                "user": UserData(email=email, code="", user_role="unknown"),
                "header": [],
                "attachments": [],
            }

        # Get the first header to determine user info
        first_header = headers[0]
        user_role = self._get_user_role(email, first_header)

        # Get all appkeys from headers
        appkeys = [header.appkey for header in headers]

        # Get items for all headers
        items = db.query(SrFctItems).filter(SrFctItems.appkey.in_(appkeys)).all()

        # Get attachments for all headers
        attachments = (
            db.query(SrFctAttachment).filter(SrFctAttachment.appkey.in_(appkeys)).all()
        )

        # Get visit data for customer info
        # keyid in sr_fct_header references appkey in fct_visits
        visit_keyids = [header.keyid for header in headers]
        visits = db.query(FctVisits).filter(FctVisits.appkey.in_(visit_keyids)).all()

        # Create a mapping of visit appkey to visit data
        visit_map = {visit.appkey: visit for visit in visits}

        # Structure the response
        structured_headers = []

        for header in headers:
            # Get visit data for this header
            visit = visit_map.get(header.keyid)

            # Get items for this header
            header_items = [item for item in items if item.appkey == header.appkey]

            # Separate return and replace items based on fk_actiontype
            return_items = [
                SrSyncItemData.from_sr_item(item)
                for item in header_items
                if item.fk_actiontype == 251
            ]

            replace_items = [
                SrSyncItemData.from_sr_item(item)
                for item in header_items
                if item.fk_actiontype == 252
            ]

            # Create header data
            header_data = SrSyncHeaderData(
                appkey=header.appkey,
                keyid=header.keyid,
                fk_typerequest=header.fk_typerequest,
                fk_reasonreturn=header.fk_reasonreturn,
                fk_modereturn=header.fk_modereturn,
                fk_status=header.fk_status,
                fk_srrtype=header.fk_srrtype,  # Changed from srr_type to match DB field
                code=header.code,
                date_sent_approval=(
                    header.date_sent_approval.isoformat()
                    if header.date_sent_approval
                    else None
                ),
                # Map FctVisits fields correctly: kunnr->customer_code, name->customer_name, address->customer_address
                customer_code=visit.kunnr if visit else "",
                customer_name=visit.name if visit else "",
                customer_address=visit.address if visit else "",
                ship_name=(
                    visit.name if visit else ""
                ),  # Same as customer_name from visits
                ship_to=(
                    visit.kunnr if visit else ""
                ),  # Same as customer_code from visits
                sdo_pao_remarks=header.sdo_pao_remarks,
                ssa_remarks=header.ssa_remarks,
                approver_remarks=header.approver_remarks,
                return_items=return_items,
                replace_items=replace_items,
            )

            structured_headers.append(header_data)

        return {
            "user": UserData(email=email, code=first_header.code, user_role=user_role),
            "header": structured_headers,
            "attachments": [
                {
                    "appkey": att.appkey,
                    "keyid": att.keyid,
                    "file_name": att.file_name
                    or att.image,  # Use file_name or fallback to image
                    "file_path": att.file_path or "",
                    "file_size": getattr(
                        att, "file_size", None
                    ),  # May not exist in current model
                    "file_type": getattr(
                        att, "file_type", None
                    ),  # May not exist in current model
                    "uploaded_at": (
                        att.created_at.isoformat() if att.created_at else None
                    ),
                }
                for att in attachments
            ],
        }


sr_sync_crud = CRUDSrSync()
