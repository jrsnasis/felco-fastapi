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
            .join(SrFctHeader, self.model.keyid == SrFctHeader.keyid)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_keyids(
        self, db: Session, *, keyids: List[str]
    ) -> List[SrFctLogsRemarksHeader]:
        """Get all header logs by list of keyids"""
        return db.query(self.model).filter(self.model.keyid.in_(keyids)).all()


sr_logsremarksheader_crud = CRUDSrLogsRemarksHeader(SrFctLogsRemarksHeader)
