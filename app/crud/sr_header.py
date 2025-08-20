# app/crud/sr_header.py
from sqlalchemy.orm import Session
from typing import List

from app.models.sr_fct_header import SrFctHeader


class CRUDSrHeader:
    def __init__(self, model):
        self.model = model

    def get_by_email(self, db: Session, *, email: str) -> List[SrFctHeader]:
        """Get all headers by fspemail or rsmemail"""
        return (
            db.query(self.model)
            .filter((self.model.fspemail == email) | (self.model.rsmemail == email))
            .all()
        )

    def get_by_keyid(self, db: Session, *, keyid: str) -> List[SrFctHeader]:
        """Get headers by keyid (references fct_visits.appkey)"""
        return db.query(self.model).filter(self.model.keyid == keyid).all()

    def count_by_email(self, db: Session, *, email: str) -> int:
        """Count headers by fspemail or rsmemail"""
        return (
            db.query(self.model)
            .filter((self.model.fspemail == email) | (self.model.rsmemail == email))
            .count()
        )


sr_header_crud = CRUDSrHeader(SrFctHeader)
