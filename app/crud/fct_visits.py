# app/crud/fct_visits.py
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from datetime import date

from app.crud.base import CRUDBase
from app.models.fct_visits import FctVisits
from app.schemas.fct_visits import FctVisitsCreate, FctVisitsBase


class CRUDFctVisits(CRUDBase[FctVisits, FctVisitsCreate, FctVisitsBase]):
    def get_by_appkey(self, db: Session, *, appkey: str) -> Optional[FctVisits]:
        """Get visit by appkey"""
        return db.query(self.model).filter(self.model.appkey == appkey).first()

    def get_multi_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        empid: Optional[int] = None,
        code: Optional[str] = None,
        kunnr: Optional[str] = None,
        vtype: Optional[str] = None,
        vdate_from: Optional[date] = None,
        vdate_to: Optional[date] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> List[FctVisits]:
        """Get multiple visits with filtering and search"""
        query = db.query(self.model)

        # Apply filters
        if search:
            query = query.filter(
                or_(
                    self.model.appkey.ilike(f"%{search}%"),
                    self.model.name.ilike(f"%{search}%"),
                    self.model.kunnr.ilike(f"%{search}%"),
                    self.model.address.ilike(f"%{search}%"),
                )
            )

        if empid:
            query = query.filter(self.model.empid == empid)

        if code:
            query = query.filter(self.model.code == code)

        if kunnr:
            query = query.filter(self.model.kunnr == kunnr)

        if vtype:
            query = query.filter(self.model.vtype == vtype)

        if vdate_from and vdate_to:
            query = query.filter(
                and_(self.model.vdate >= vdate_from, self.model.vdate <= vdate_to)
            )
        elif vdate_from:
            query = query.filter(self.model.vdate >= vdate_from)
        elif vdate_to:
            query = query.filter(self.model.vdate <= vdate_to)

        # Apply sorting
        if sort_by and hasattr(self.model, sort_by):
            order_column = getattr(self.model, sort_by)
            if sort_order.lower() == "desc":
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
        else:
            query = query.order_by(self.model.vdate.desc())

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        search: Optional[str] = None,
        empid: Optional[int] = None,
        code: Optional[str] = None,
        kunnr: Optional[str] = None,
        vtype: Optional[str] = None,
        vdate_from: Optional[date] = None,
        vdate_to: Optional[date] = None,
    ) -> int:
        """Get count of visits with filters"""
        query = db.query(func.count(self.model.appkey))

        # Apply same filters as get_multi_with_filters
        if search:
            query = query.filter(
                or_(
                    self.model.appkey.ilike(f"%{search}%"),
                    self.model.name.ilike(f"%{search}%"),
                    self.model.kunnr.ilike(f"%{search}%"),
                    self.model.address.ilike(f"%{search}%"),
                )
            )

        if empid:
            query = query.filter(self.model.empid == empid)

        if code:
            query = query.filter(self.model.code == code)

        if kunnr:
            query = query.filter(self.model.kunnr == kunnr)

        if vtype:
            query = query.filter(self.model.vtype == vtype)

        if vdate_from and vdate_to:
            query = query.filter(
                and_(self.model.vdate >= vdate_from, self.model.vdate <= vdate_to)
            )
        elif vdate_from:
            query = query.filter(self.model.vdate >= vdate_from)
        elif vdate_to:
            query = query.filter(self.model.vdate <= vdate_to)

        return query.scalar()

    def get_by_customer_and_date(
        self, db: Session, *, kunnr: str, vdate: date
    ) -> List[FctVisits]:
        """Get visits by customer and date"""
        return (
            db.query(self.model)
            .filter(self.model.kunnr == kunnr, self.model.vdate == vdate)
            .all()
        )

    def get_by_employee(self, db: Session, *, empid: int) -> List[FctVisits]:
        """Get visits by employee ID"""
        return db.query(self.model).filter(self.model.empid == empid).all()

    def get_recent_visits(
        self, db: Session, *, days: int = 7, limit: int = 100
    ) -> List[FctVisits]:
        """Get recent visits within specified days"""
        from datetime import datetime, timedelta

        cutoff_date = datetime.now().date() - timedelta(days=days)

        return (
            db.query(self.model)
            .filter(self.model.vdate >= cutoff_date)
            .order_by(self.model.vdate.desc())
            .limit(limit)
            .all()
        )


fct_visits = CRUDFctVisits(FctVisits)
