# app/crud/sr_attachment.py
from sqlalchemy.orm import Session
from typing import List

from app.models.sr_fct_attachment import SrFctAttachment
from app.models.sr_fct_header import SrFctHeader


class CRUDSrAttachment:
    def __init__(self, model):
        self.model = model

    def get_by_email(self, db: Session, *, email: str) -> List[SrFctAttachment]:
        """Get all attachments by email through sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctHeader, self.model.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_appkeys(
        self, db: Session, *, appkeys: List[str]
    ) -> List[SrFctAttachment]:
        """Get all attachments by list of appkeys"""
        return db.query(self.model).filter(self.model.appkey.in_(appkeys)).all()

    def count_by_email(self, db: Session, *, email: str) -> int:
        """Count attachments by email through sr_fct_header relationship"""
        return (
            db.query(self.model)
            .join(SrFctHeader, self.model.appkey == SrFctHeader.appkey)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .count()
        )


sr_attachment_crud = CRUDSrAttachment(SrFctAttachment)
