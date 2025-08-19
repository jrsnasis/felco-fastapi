# app/api/v1/sr_sync.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List

from app.api.deps import get_db_session
from app.crud.sr_sync import sr_sync_crud
from app.schemas.sr_sync import SrSyncResponse
from app.schemas.fct_visits import FctVisitsResponse

router = APIRouter()


@router.get("/", response_model=SrSyncResponse)
async def get_all_sr_data_by_email(
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    keyid: Optional[str] = Query(
        None, description="Optional: Filter by specific visit keyid"
    ),
    db: Session = Depends(get_db_session),
):
    """Get all sales return data by email (and optionally by keyid) in one call"""
    try:
        sr_data = sr_sync_crud.get_all_sr_data_by_email(db=db, email=email, keyid=keyid)

        return SrSyncResponse(
            headers=sr_data["headers"],
            items=sr_data["items"],
            attachments=sr_data["attachments"],
            header_logs=sr_data["header_logs"],
            items_logs=sr_data["items_logs"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch SR data: {str(e)}",
        )


@router.get("/counts", response_model=Dict[str, int])
async def get_sr_data_counts_by_email(
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    db: Session = Depends(get_db_session),
):
    """Get counts of all SR data by email"""
    try:
        return sr_sync_crud.get_counts_by_email(db=db, email=email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch SR data counts: {str(e)}",
        )


@router.get("/visits", response_model=List[FctVisitsResponse])
async def get_visits_by_email(
    email: str = Query(..., description="Filter by fspemail or rsmemail"),
    db: Session = Depends(get_db_session),
):
    """Get fct_visits data by email for reference"""
    try:
        visits = sr_sync_crud.get_visits_by_email(db=db, email=email)
        return visits
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch visits data: {str(e)}",
        )
