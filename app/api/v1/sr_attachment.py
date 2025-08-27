# app/api/v1/sr_attachment.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db_session
from app.crud.sr_attachment import sr_attachment_crud
from app.schemas.sr_fct_attachment import SrFctAttachmentResponse
from app.schemas.base import SuccessResponse
from app.core.exceptions import InvalidEmailException, SRAttachmentNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[SrFctAttachmentResponse]])
async def get_sr_attachments_by_email(
    request: Request,
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return attachments by email"""
    # Validate email format
    if not email or "@" not in email:
        raise InvalidEmailException(email)

    # Get data from database
    attachments = sr_attachment_crud.get_by_email(db=db, email=email)

    # Check if data exists
    if not attachments:
        raise SRAttachmentNotFoundException(f"email: {email}")

    return SuccessResponse(
        data=attachments,
        message="Successfully retrieved Sales Return attachments",
        count=len(attachments),
    )
