# app/crud/sr_header.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.sr_fct_header import SrFctHeader
from app.schemas.sr_fct_header import SrFctHeaderCreate, SrFctHeaderUpdate


class CRUDSrHeader:
    def __init__(self, model):
        self.model = model

    def create(self, db: Session, *, obj_in: SrFctHeaderCreate) -> SrFctHeader:
        """Create a new header"""
        # Convert Pydantic model to dict
        obj_data = obj_in.model_dump()

        # Add timestamps
        now = datetime.utcnow()
        obj_data.update(
            {
                "created_at": now,
                "updated_at": now,
                "m_created_at": now,
                "m_updated_at": now,
            }
        )

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[SrFctHeader]:
        """Get header by ID"""
        return db.query(self.model).filter(self.model.id == id).first()

    def get_by_appkey(self, db: Session, *, appkey: str) -> Optional[SrFctHeader]:
        """Get header by appkey"""
        return db.query(self.model).filter(self.model.appkey == appkey).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[SrFctHeader]:
        """Get multiple headers with pagination"""
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(
        self, db: Session, *, db_obj: SrFctHeader, obj_in: SrFctHeaderUpdate
    ) -> SrFctHeader:
        """Update a header"""
        # Get only non-None values from update schema
        update_data = obj_in.model_dump(exclude_unset=True)

        # Add update timestamp
        update_data["updated_at"] = datetime.utcnow()
        update_data["m_updated_at"] = datetime.utcnow()

        # Update object attributes
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[SrFctHeader]:
        """Delete a header"""
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def count(self, db: Session) -> int:
        """Count total headers"""
        return db.query(self.model).count()

    # Business-specific methods
    def get_by_kunnr(self, db: Session, *, kunnr: str) -> List[SrFctHeader]:
        """Get headers by customer number"""
        return db.query(self.model).filter(self.model.kunnr == kunnr).all()

    def get_by_status(self, db: Session, *, status_id: int) -> List[SrFctHeader]:
        """Get headers by status"""
        return db.query(self.model).filter(self.model.fk_status == status_id).all()

    def get_by_code(self, db: Session, *, code: str) -> List[SrFctHeader]:
        """Get headers by code"""
        return db.query(self.model).filter(self.model.code == code).all()

    def search(
        self,
        db: Session,
        *,
        kunnr: Optional[str] = None,
        status_id: Optional[int] = None,
        code: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[SrFctHeader]:
        """Search headers with filters"""
        query = db.query(self.model)

        if kunnr:
            query = query.filter(self.model.kunnr == kunnr)
        if status_id:
            query = query.filter(self.model.fk_status == status_id)
        if code:
            query = query.filter(self.model.code == code)

        return query.offset(skip).limit(limit).all()


# Create the CRUD instance
sr_header_crud = CRUDSrHeader(SrFctHeader)
