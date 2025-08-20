# app/crud/fct_visits.py
from sqlalchemy.orm import Session
from typing import List

from app.models.fct_visits import FctVisits


class CRUDFctVisits:
    def __init__(self, model):
        self.model = model

    def get_by_email(self, db: Session, *, email: str) -> List[FctVisits]:
        """Get all visits by fspemail or rsmemail"""
        return (
            db.query(self.model)
            .filter((self.model.fspemail == email) | (self.model.rsmemail == email))
            .all()
        )

    def get_keyids_by_email(self, db: Session, *, email: str) -> List[str]:
        """Get all keyids for visits by email (for SR header reference)"""
        visits = self.get_by_email(db=db, email=email)
        return [visit.appkey for visit in visits]


fct_visits_crud = CRUDFctVisits(FctVisits)
