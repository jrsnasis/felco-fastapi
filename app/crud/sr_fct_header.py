# app/crud/sr_fct_header.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.crud.base import CRUDBase
from app.models.sr_fct_header import SrFctHeader
from app.schemas.sr_fct_header import SrFctHeaderCreate, SrFctHeaderBase


class CRUDSrFctHeader(CRUDBase[SrFctHeader, SrFctHeaderCreate, SrFctHeaderBase]):
    def get_by_appkey(self, db: Session, *, appkey: str) -> Optional[SrFctHeader]:
        """Get SR header by appkey"""
        return db.query(self.model).filter(self.model.appkey == appkey).first()

    def get_multi_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        kunnr: Optional[str] = None,
        code: Optional[str] = None,
        fk_status: Optional[int] = None,
        created_by: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> List[SrFctHeader]:
        """Get multiple SR headers with filtering and search"""
        query = db.query(self.model)

        # Apply filters
        if search:
            query = query.filter(
                or_(
                    self.model.appkey.ilike(f"%{search}%"),
                    self.model.ship_name.ilike(f"%{search}%"),
                    self.model.kunnr.ilike(f"%{search}%"),
                    self.model.created_by.ilike(f"%{search}%"),
                )
            )

        if kunnr:
            query = query.filter(self.model.kunnr == kunnr)

        if code:
            query = query.filter(self.model.code == code)

        if fk_status:
            query = query.filter(self.model.fk_status == fk_status)

        if created_by:
            query = query.filter(self.model.created_by == created_by)

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            order_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        else:
            query = query.order_by(self.model.created_at.desc())

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        search: Optional[str] = None,
        kunnr: Optional[str] = None,
        code: Optional[str] = None,
        fk_status: Optional[int] = None,
        created_by: Optional[str] = None,
    ) -> int:
        """Get count of SR headers with filters"""
        query = db.query(func.count(self.model.id))

        # Apply same filters as get_multi_with_filters
        if search:
            query = query.filter(
                or_(
                    self.model.appkey.ilike(f"%{search}%"),
                    self.model.ship_name.ilike(f"%{search}%"),
                    self.model.kunnr.ilike(f"%{search}%"),
                    self.model.created_by.ilike(f"%{search}%"),
                )
            )

        if kunnr:
            query = query.filter(self.model.kunnr == kunnr)

        if code:
            query = query.filter(self.model.code == code)

        if fk_status:
            query = query.filter(self.model.fk_status == fk_status)

        if created_by:
            query = query.filter(self.model.created_by == created_by)

        return query.scalar()

    def get_with_items(self, db: Session, *, appkey: str) -> Optional[SrFctHeader]:
        """Get SR header with its items"""
        from app.models.sr_fct_items import SrFctItems

        return (
            db.query(self.model)
            .filter(self.model.appkey == appkey)
            .join(SrFctItems, SrFctItems.appkey == self.model.appkey, isouter=True)
            .first()
        )

    def get_by_customer_and_code(
        self, db: Session, *, kunnr: str, code: str
    ) -> List[SrFctHeader]:
        """Get SR headers by customer number and code"""
        return (
            db.query(self.model)
            .filter(self.model.kunnr == kunnr, self.model.code == code)
            .all()
        )


sr_fct_header = CRUDSrFctHeader(SrFctHeader)
