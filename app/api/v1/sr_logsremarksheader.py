# app/api/v1/sr_logsremarksheader.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db_session
from app.crud.sr_logsremarksheader import sr_logsremarksheader_crud
from app.schemas.sr_fct_logsremarksheader import SrFctLogsRemarksHeaderResponse
from app.schemas.base import SuccessResponse
from app.core.exceptions import InvalidEmailException, SRNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[SrFctLogsRemarksHeaderResponse]])
async def get_sr_header_logs_by_email(
    request: Request,
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return header logs by email"""
    # Validate email format
    if not email or "@" not in email:
        raise InvalidEmailException(email)

    # Get data from database
    header_logs = sr_logsremarksheader_crud.get_by_email(db=db, email=email)

    # Check if data exists
    if not header_logs:
        raise SRNotFoundException("Header Logs", f"email: {email}")

    return SuccessResponse(
        data=header_logs,
        message="Successfully retrieved Sales Return header logs",
    )
