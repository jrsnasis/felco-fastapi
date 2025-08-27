# app/api/v1/sr_header.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db_session
from app.crud.sr_header import sr_header_crud
from app.schemas.sr_fct_header import SrFctHeaderResponse
from app.schemas.base import SuccessResponse
from app.core.exceptions import InvalidEmailException, SRHeaderNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[SrFctHeaderResponse]])
async def get_sr_headers_by_email(
    request: Request,
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return headers by email"""
    # Validate email format
    if not email or "@" not in email:
        raise InvalidEmailException(email)

    # Get data from database
    headers = sr_header_crud.get_by_email(db=db, email=email)

    # Check if data exists
    if not headers:
        raise SRHeaderNotFoundException(f"email: {email}")

    return SuccessResponse(
        data=headers,
        message="Successfully retrieved Sales Return headers",
    )
