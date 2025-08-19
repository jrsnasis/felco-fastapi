# app/api/v1/sr_logsremarksitems.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.crud.sr_logsremarksitems import sr_logsremarksitems_crud
from app.schemas.sr_fct_logsremarksitems import SrFctLogsRemarksItemsResponse

router = APIRouter()


@router.get("/", response_model=List[SrFctLogsRemarksItemsResponse])
async def get_sr_items_logs_by_email(
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return items logs by email"""
    items_logs = sr_logsremarksitems_crud.get_by_email(db=db, email=email)
    return items_logs
