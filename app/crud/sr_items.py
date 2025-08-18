# app/crud/sr_items.py
from sqlalchemy.orm import Session
from typing import List

from app.crud.base import CRUDBase
from app.models.sr_fct_items import SrFctItems
from app.schemas.sr_fct_items import SrFctItemsCreate, SrFctItemsUpdate


class CRUDSrItems(CRUDBase[SrFctItems, SrFctItemsCreate, SrFctItemsUpdate]):
    def get_by_appkey(self, db: Session, *, appkey: str) -> List[SrFctItems]:
        """Get all items by appkey"""
        return db.query(SrFctItems).filter(SrFctItems.appkey == appkey).all()

    def get_by_material(self, db: Session, *, matnr: str) -> List[SrFctItems]:
        """Get all items by material number"""
        return db.query(SrFctItems).filter(SrFctItems.matnr == matnr).all()

    def count(self, db: Session) -> int:
        """Count total items"""
        return db.query(SrFctItems).count()


sr_items_crud = CRUDSrItems(SrFctItems)
