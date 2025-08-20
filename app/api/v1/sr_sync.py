# app/api/v1/sr_sync.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
import logging

from app.api.deps import get_db_session
from app.crud.sr_sync import sr_sync_crud
from app.schemas.sr_sync import SrSyncResponse
from app.schemas.fct_visits import FctVisitsResponse
from app.core.exceptions import (
    InvalidEmailException, 
    InvalidKeyIdException, 
    SRNotFoundException
)
from app.schemas.base import SuccessResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[SrSyncResponse])
async def get_all_sr_data_by_email(
    request: Request,
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    keyid: Optional[str] = Query(None, description="Optional: Filter by specific visit keyid"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return data by email (and optionally by keyid) in one call"""
    # Validate email
    if not email or "@" not in email:
        raise InvalidEmailException(email)
    
    # Validate keyid if provided
    if keyid and not keyid.strip():
        raise InvalidKeyIdException(keyid)
    
    # Get data from database
    sr_data = sr_sync_crud.get_all_sr_data_by_email(db=db, email=email, keyid=keyid)
    
    # Check if any data was found
    if not any([
        sr_data["headers"],
        sr_data["items"], 
        sr_data["attachments"],
        sr_data["header_logs"],
        sr_data["items_logs"]
    ]):
        identifier = f"email: {email}"
        if keyid:
            identifier += f", keyid: {keyid}"
        raise SRNotFoundException("data", identifier)

    sync_response = SrSyncResponse(
        headers=sr_data["headers"],
        items=sr_data["items"],
        attachments=sr_data["attachments"],
        header_logs=sr_data["header_logs"],
        items_logs=sr_data["items_logs"],
    )
    
    # Calculate total records
    total_count = (
        len(sr_data["headers"]) + 
        len(sr_data["items"]) + 
        len(sr_data["attachments"]) + 
        len(sr_data["header_logs"]) + 
        len(sr_data["items_logs"])
    )
    
    return SuccessResponse(
        data=sync_response,
        message="Successfully retrieved all Sales Return data",
        count=total_count
    )


@router.get("/counts", response_model=SuccessResponse[Dict[str, int]])
async def get_sr_data_counts_by_email(
    request: Request,
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    db: Session = Depends(get_db_session),
):
    """Get counts of all SR data by email"""
    if not email or "@" not in email:
        raise InvalidEmailException(email)
    
    counts = sr_sync_crud.get_counts_by_email(db=db, email=email)
    
    return SuccessResponse(
        data=counts,
        message="Successfully retrieved Sales Return data counts",
        count=sum(counts.values())
    )


@router.get("/visits", response_model=SuccessResponse[List[FctVisitsResponse]])
async def get_visits_by_email(
    request: Request,
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    db: Session = Depends(get_db_session),
):
    """Get fct_visits data by email for reference"""
    if not email or "@" not in email:
        raise InvalidEmailException(email)
    
    visits = sr_sync_crud.get_visits_by_email(db=db, email=email)
    
    # Check if data exists
    if not visits:
        raise SRNotFoundException("visits", f"email: {email}")
    
    return SuccessResponse(
        data=visits,
        message="Successfully retrieved visits data",
        count=len(visits)
    )