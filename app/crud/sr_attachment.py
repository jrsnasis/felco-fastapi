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
            .join(SrFctHeader, self.model.keyid == SrFctHeader.keyid)
            .filter((SrFctHeader.fspemail == email) | (SrFctHeader.rsmemail == email))
            .all()
        )

    def get_by_keyid(self, db: Session, *, keyids: List[str]) -> List[SrFctAttachment]:
        """Get all attachments by list of keyids"""
        return db.query(self.model).filter(self.model.keyid.in_(keyids)).all()


sr_attachment_crud = CRUDSrAttachment(SrFctAttachment)
