# app/api/v1/sr_header.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db_session
from app.crud.sr_header import sr_header_crud
from app.schemas.sr_fct_header import (
    SrFctHeaderCreate,
    SrFctHeaderUpdate,
    SrFctHeaderResponse,
    SrFctHeaderListResponse,
)

router = APIRouter()


@router.post(
    "/", response_model=SrFctHeaderResponse, status_code=status.HTTP_201_CREATED
)
async def create_sr_header(
    header_data: SrFctHeaderCreate, db: Session = Depends(get_db_session)
):
    """Create a new sales return header"""
    # Check if appkey already exists
    existing_header = sr_header_crud.get_by_appkey(db=db, appkey=header_data.appkey)
    if existing_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Header with appkey '{header_data.appkey}' already exists",
        )

    try:
        return sr_header_crud.create(db=db, obj_in=header_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create header: {str(e)}",
        )


@router.get("/{header_id}", response_model=SrFctHeaderResponse)
async def get_sr_header(header_id: int, db: Session = Depends(get_db_session)):
    """Get a specific sales return header by ID"""
    header = sr_header_crud.get(db=db, id=header_id)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Header not found"
        )
    return header


@router.get("/appkey/{appkey}", response_model=SrFctHeaderResponse)
async def get_sr_header_by_appkey(appkey: str, db: Session = Depends(get_db_session)):
    """Get a specific sales return header by appkey"""
    header = sr_header_crud.get_by_appkey(db=db, appkey=appkey)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Header with appkey '{appkey}' not found",
        )
    return header


@router.get("/", response_model=SrFctHeaderListResponse)
async def get_sr_headers(
    skip: int = 0,
    limit: int = 100,
    kunnr: Optional[str] = Query(None, description="Filter by customer number"),
    status_id: Optional[int] = Query(None, description="Filter by status ID"),
    code: Optional[str] = Query(None, description="Filter by code"),
    db: Session = Depends(get_db_session),
):
    """Get list of sales return headers with pagination and optional filters"""

    # Apply filters if provided
    if kunnr or status_id or code:
        headers = sr_header_crud.search(
            db=db, kunnr=kunnr, status_id=status_id, code=code, skip=skip, limit=limit
        )
    else:
        headers = sr_header_crud.get_multi(db=db, skip=skip, limit=limit)

    total = sr_header_crud.count(db=db)

    return SrFctHeaderListResponse(items=headers, total=total, skip=skip, limit=limit)


@router.put("/{header_id}", response_model=SrFctHeaderResponse)
async def update_sr_header(
    header_id: int,
    header_update: SrFctHeaderUpdate,
    db: Session = Depends(get_db_session),
):
    """Update a sales return header"""
    header = sr_header_crud.get(db=db, id=header_id)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Header not found"
        )

    try:
        return sr_header_crud.update(db=db, db_obj=header, obj_in=header_update)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update header: {str(e)}",
        )


@router.delete("/{header_id}")
async def delete_sr_header(header_id: int, db: Session = Depends(get_db_session)):
    """Delete a sales return header"""
    header = sr_header_crud.get(db=db, id=header_id)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Header not found"
        )

    try:
        sr_header_crud.remove(db=db, id=header_id)
        return {"message": "Header deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete header: {str(e)}",
        )


# Additional simple endpoints
@router.get("/customer/{kunnr}", response_model=List[SrFctHeaderResponse])
async def get_headers_by_customer(kunnr: str, db: Session = Depends(get_db_session)):
    """Get all headers for a specific customer"""
    return sr_header_crud.get_by_kunnr(db=db, kunnr=kunnr)


@router.get("/status/{status_id}", response_model=List[SrFctHeaderResponse])
async def get_headers_by_status(status_id: int, db: Session = Depends(get_db_session)):
    """Get all headers with a specific status"""
    return sr_header_crud.get_by_status(db=db, status_id=status_id)
