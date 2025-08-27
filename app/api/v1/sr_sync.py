# app/api/v1/sr_sync.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.api.deps import get_db_session
from app.crud.sr_sync import sr_sync_crud
from app.schemas.sr_sync import SrSyncResponse
from app.core.exceptions import (
    InvalidEmailException,
    InvalidKeyIdException,
    SRNotFoundException,
)
from app.schemas.base import SuccessResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[SrSyncResponse])
async def get_sr_data_by_email(
    request: Request,
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    keyid: Optional[str] = Query(
        None, description="Optional: Filter by specific visit keyid"
    ),
    db: Session = Depends(get_db_session),
):
    """Get all sales return data by email in the required JSON format (ssaemail support removed for now)"""
    # Validate email
    if not email or "@" not in email:
        raise InvalidEmailException(email)

    # Validate keyid if provided
    if keyid and not keyid.strip():
        raise InvalidKeyIdException(keyid)

    # Get data from database
    sr_data = sr_sync_crud.get_sr_data_by_email(db=db, email=email, keyid=keyid)

    # Check if any data was found
    if not sr_data["header"] and not sr_data["attachments"]:
        identifier = f"email: {email}"
        if keyid:
            identifier += f", keyid: {keyid}"
        raise SRNotFoundException("data", identifier)

    # Create the response
    sync_response = SrSyncResponse(
        user=sr_data["user"],
        header=sr_data["header"],
        attachments=sr_data["attachments"],
    )

    return SuccessResponse(
        data=sync_response,
        message="Successfully retrieved all Sales Return data",
    )
