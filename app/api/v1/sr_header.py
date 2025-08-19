# app/api/v1/sr_header.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.crud.sr_header import sr_header_crud
from app.schemas.sr_fct_header import SrFctHeaderResponse

router = APIRouter()


@router.get("/", response_model=List[SrFctHeaderResponse])
async def get_sr_headers_by_email(
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return headers by email"""
    headers = sr_header_crud.get_by_email(db=db, email=email)
    return headers
