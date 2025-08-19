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
            .join(SrFctItems, self.model.appkey == SrFctItems.appkey)
            .join(SrFctHeader, SrFctItems.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_appkeys(
        self, db: Session, *, appkeys: List[str]
    ) -> List[SrFctLogsRemarksItems]:
        """Get all items logs by list of appkeys"""
        return db.query(self.model).filter(self.model.appkey.in_(appkeys)).all()

    def count_by_email(self, db: Session, *, email: str) -> int:
        """Count items logs by email through sr_fct_items -> sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctItems, self.model.appkey == SrFctItems.appkey)
            .join(SrFctHeader, SrFctItems.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .count()
        )


sr_logsremarksitems_crud = CRUDSrLogsRemarksItems(SrFctLogsRemarksItems)
