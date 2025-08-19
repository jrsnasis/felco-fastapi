# app/api/v1/sr_items.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.crud.sr_items import sr_items_crud
from app.schemas.sr_fct_items import SrFctItemsResponse

router = APIRouter()


@router.get("/", response_model=List[SrFctItemsResponse])
async def get_sr_items_by_email(
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return items by email"""
    items = sr_items_crud.get_by_email(db=db, email=email)
    return items
