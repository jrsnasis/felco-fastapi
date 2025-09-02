# app/crud/sr_logsremarksitems.py
from sqlalchemy.orm import Session
from typing import List

from app.models.sr_fct_logsremarksitems import SrFctLogsRemarksItems
from app.models.sr_fct_items import SrFctItems
from app.models.sr_fct_header import SrFctHeader


class CRUDSrLogsRemarksItems:
    def __init__(self, model):
        self.model = model

    def get_by_email(self, db: Session, *, email: str) -> List[SrFctLogsRemarksItems]:
        """Get all items logs by email through sr_fct_items -> sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctItems, self.model.keyid == SrFctItems.keyid)
            .join(SrFctHeader, SrFctItems.keyid == SrFctHeader.keyid)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_keyids(
        self, db: Session, *, keyids: List[str]
    ) -> List[SrFctLogsRemarksItems]:
        """Get all items logs by list of keyids"""
        return db.query(self.model).filter(self.model.keyid.in_(keyids)).all()


sr_logsremarksitems_crud = CRUDSrLogsRemarksItems(SrFctLogsRemarksItems)
