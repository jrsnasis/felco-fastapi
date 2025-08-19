# app/crud/sr_logsremarksheader.py
from sqlalchemy.orm import Session
from typing import List

from app.models.sr_fct_logsremarksheader import SrFctLogsRemarksHeader
from app.models.sr_fct_header import SrFctHeader


class CRUDSrLogsRemarksHeader:
    def __init__(self, model):
        self.model = model

    def get_by_email(self, db: Session, *, email: str) -> List[SrFctLogsRemarksHeader]:
        """Get all header logs by email through sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctHeader, self.model.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_appkeys(
        self, db: Session, *, appkeys: List[str]
    ) -> List[SrFctLogsRemarksHeader]:
        """Get all header logs by list of appkeys"""
        return db.query(self.model).filter(self.model.appkey.in_(appkeys)).all()

    def count_by_email(self, db: Session, *, email: str) -> int:
        """Count header logs by email through sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctHeader, self.model.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .count()
        )


sr_logsremarksheader_crud = CRUDSrLogsRemarksHeader(SrFctLogsRemarksHeader)
