# app/crud/sr_fct_items.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.sr_fct_items import SrFctItems
from app.schemas.sr_fct_items import SrFctItemsCreate, SrFctItemsBase


class CRUDSrFctItems(CRUDBase[SrFctItems, SrFctItemsCreate, SrFctItemsBase]):
    def get_by_appkey(self, db: Session, *, appkey: str) -> List[SrFctItems]:
        """Get all items for a specific SR header by appkey"""
        return db.query(self.model).filter(self.model.appkey == appkey).all()

    def get_by_material(self, db: Session, *, matnr: str) -> List[SrFctItems]:
        """Get all items for a specific material"""
        return db.query(self.model).filter(self.model.matnr == matnr).all()

    def get_count_by_appkey(self, db: Session, *, appkey: str) -> int:
        """Get count of items for a specific SR header"""
        return (
            db.query(func.count(self.model.id))
            .filter(self.model.appkey == appkey)
            .scalar()
        )

    def get_total_amount_by_appkey(self, db: Session, *, appkey: str) -> float:
        """Get total amount for all items in an SR header"""
        result = (
            db.query(func.sum(self.model.total_amount))
            .filter(self.model.appkey == appkey)
            .scalar()
        )
        return float(result) if result else 0.0

    def get_by_action_type(
        self, db: Session, *, fk_actiontype: int
    ) -> List[SrFctItems]:
        """Get items by action type"""
        return (
            db.query(self.model).filter(self.model.fk_actiontype == fk_actiontype).all()
        )

    def delete_by_appkey(self, db: Session, *, appkey: str) -> int:
        """Delete all items for a specific SR header"""
        deleted_count = (
            db.query(self.model).filter(self.model.appkey == appkey).delete()
        )
        db.commit()
        return deleted_count

    def bulk_create(
        self, db: Session, *, items: List[SrFctItemsCreate]
    ) -> List[SrFctItems]:
        """Create multiple items in bulk"""
        db_items = []
        for item in items:
            db_item = self.model(**item.model_dump())
            db_items.append(db_item)

        db.add_all(db_items)
        db.commit()

        for db_item in db_items:
            db.refresh(db_item)

        return db_items


sr_fct_items = CRUDSrFctItems(SrFctItems)
