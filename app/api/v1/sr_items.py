# app/api/v1/sr_items.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# from typing import List

from app.api.deps import get_db_session
from app.crud.sr_items import sr_items_crud
from app.schemas.sr_fct_items import (
    SrFctItemsCreate,
    SrFctItemsResponse,
    SrFctItemsListResponse,
)

router = APIRouter()


@router.post(
    "/", response_model=SrFctItemsResponse, status_code=status.HTTP_201_CREATED
)
async def create_sr_item(
    item_data: SrFctItemsCreate, db: Session = Depends(get_db_session)
):
    """Create a new sales return item"""
    try:
        return sr_items_crud.create(db=db, obj_in=item_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create item: {str(e)}",
        )


@router.get("/{item_id}", response_model=SrFctItemsResponse)
async def get_sr_item(item_id: int, db: Session = Depends(get_db_session)):
    """Get a specific sales return item by ID"""
    item = sr_items_crud.get(db=db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.get("/", response_model=SrFctItemsListResponse)
async def get_sr_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)
):
    """Get list of sales return items with pagination"""
    items = sr_items_crud.get_multi(db=db, skip=skip, limit=limit)
    total = sr_items_crud.count(db=db)

    return SrFctItemsListResponse(items=items, total=total, skip=skip, limit=limit)
