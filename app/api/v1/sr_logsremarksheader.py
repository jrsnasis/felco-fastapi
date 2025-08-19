# app/api/v1/sr_logsremarksheader.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.crud.sr_logsremarksheader import sr_logsremarksheader_crud
from app.schemas.sr_fct_logsremarksheader import SrFctLogsRemarksHeaderResponse

router = APIRouter()


@router.get("/", response_model=List[SrFctLogsRemarksHeaderResponse])
async def get_sr_header_logs_by_email(
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return header logs by email"""
    header_logs = sr_logsremarksheader_crud.get_by_email(db=db, email=email)
    return header_logs
