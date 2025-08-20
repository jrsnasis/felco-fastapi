# app/api/v1/sr_items.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db_session
from app.crud.sr_items import sr_items_crud
from app.schemas.sr_fct_items import SrFctItemsResponse
from app.schemas.base import SuccessResponse
from app.core.exceptions import InvalidEmailException, SRItemsNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[SrFctItemsResponse]])
async def get_sr_items_by_email(
    request: Request,
    email: str = Query(..., description="Filter by email"),
    db: Session = Depends(get_db_session),
):
    """Get all sales return items by email"""
    # Validate email format
    if not email or "@" not in email:
        raise InvalidEmailException(email)
    
    # Get data from database
    items = sr_items_crud.get_by_email(db=db, email=email)
    
    # Check if data exists
    if not items:
        raise SRItemsNotFoundException(f"email: {email}")
    
    return SuccessResponse(
        data=items,
        message="Successfully retrieved Sales Return items",
        count=len(items)
    )