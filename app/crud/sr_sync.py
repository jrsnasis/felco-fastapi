# app/crud/sr_sync.py
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional

from app.crud.sr_header import sr_header_crud
from app.crud.sr_items import sr_items_crud
from app.crud.sr_attachment import sr_attachment_crud
from app.crud.sr_logsremarksheader import sr_logsremarksheader_crud
from app.crud.sr_logsremarksitems import sr_logsremarksitems_crud
from app.crud.fct_visits import fct_visits_crud


class CRUDSrSync:
    """CRUD operations for getting all SR data in one call"""

    def get_all_sr_data_by_email(
        self, db: Session, *, email: str, keyid: Optional[str] = None
    ) -> Dict[str, List[Any]]:
        """Get all SR data by email in one call"""

        # If keyid is provided, filter by specific visit
        if keyid:
            # Get SR data by specific keyid (from fct_visits.appkey -> sr_fct_header.keyid)
            headers = sr_header_crud.get_by_keyid(db=db, keyid=keyid)

            if headers:
                # Get related data using the appkeys from headers
                appkeys = [header.appkey for header in headers]
                items = sr_items_crud.get_by_appkeys(db=db, appkeys=appkeys)
                attachments = sr_attachment_crud.get_by_appkeys(db=db, appkeys=appkeys)
                header_logs = sr_logsremarksheader_crud.get_by_appkeys(
                    db=db, appkeys=appkeys
                )
                items_logs = sr_logsremarksitems_crud.get_by_appkeys(
                    db=db, appkeys=appkeys
                )
            else:
                items = attachments = header_logs = items_logs = []
        else:
            # Get all SR data by email
            headers = sr_header_crud.get_by_email(db=db, email=email)
            items = sr_items_crud.get_by_email(db=db, email=email)
            attachments = sr_attachment_crud.get_by_email(db=db, email=email)
            header_logs = sr_logsremarksheader_crud.get_by_email(db=db, email=email)
            items_logs = sr_logsremarksitems_crud.get_by_email(db=db, email=email)

        return {
            "headers": headers,
            "items": items,
            "attachments": attachments,
            "header_logs": header_logs,
            "items_logs": items_logs,
        }

    def get_counts_by_email(self, db: Session, *, email: str) -> Dict[str, int]:
        """Get count of all SR data by email"""
        return {
            "headers_count": sr_header_crud.count_by_email(db=db, email=email),
            "items_count": sr_items_crud.count_by_email(db=db, email=email),
            "attachments_count": sr_attachment_crud.count_by_email(db=db, email=email),
            "header_logs_count": sr_logsremarksheader_crud.count_by_email(
                db=db, email=email
            ),
            "items_logs_count": sr_logsremarksitems_crud.count_by_email(
                db=db, email=email
            ),
        }

    def get_visits_by_email(self, db: Session, *, email: str) -> List[Any]:
        """Get fct_visits data by email for reference"""
        return fct_visits_crud.get_by_email(db=db, email=email)


sr_sync_crud = CRUDSrSync()
