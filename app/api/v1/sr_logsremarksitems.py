# app/api/v1/sr_logsremarksitems.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db_session
from app.crud.sr_logsremarksitems import sr_logsremarksitems_crud
from app.schemas.sr_fct_logsremarksitems import SrFctLogsRemarksItemsResponse
from app.schemas.base import SuccessResponse
from app.core.exceptions import InvalidEmailException, SRNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[SrFctLogsRemarksItemsResponse]])
async def get_sr_items_logs_by_email(
    request: Request,
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return items logs by email"""
    # Validate email format
    if not email or "@" not in email:
        raise InvalidEmailException(email)

    # Get data from database
    items_logs = sr_logsremarksitems_crud.get_by_email(db=db, email=email)

    # Check if data exists
    if not items_logs:
        raise SRNotFoundException("Items Logs", f"email: {email}")

    return SuccessResponse(
        data=items_logs,
        message="Successfully retrieved Sales Return items logs",
        count=len(items_logs),
    )
