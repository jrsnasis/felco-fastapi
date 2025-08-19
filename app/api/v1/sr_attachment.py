# app/api/v1/sr_attachment.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_db_session
from app.crud.sr_attachment import sr_attachment_crud
from app.schemas.sr_fct_attachment import SrFctAttachmentResponse

router = APIRouter()


@router.get("/", response_model=List[SrFctAttachmentResponse])
async def get_sr_attachments_by_email(
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return attachments by email"""
    attachments = sr_attachment_crud.get_by_email(db=db, email=email)
    return attachments
