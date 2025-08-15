# app/api/v1/endpoints/sr_management.py
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import date

from app.api.deps import get_db_session, get_pagination_params
from app.schemas.base import PaginationParams
from app.schemas.fct_visits import (
    FctVisitsCreate,
    FctVisitsResponse,
    FctVisitsListResponse,
)
from app.schemas.sr_fct_header import (
    SrFctHeaderCreate,
    SrFctHeaderResponse,
    SrFctHeaderDetailResponse,
    SrFctHeaderListResponse,
)
from app.schemas.sr_fct_items import (
    SrFctItemsCreate,
    SrFctItemsResponse,
    SrFctItemsListResponse,
)
from app.crud.fct_visits import fct_visits
from app.crud.sr_fct_header import sr_fct_header
from app.crud.sr_fct_items import sr_fct_items
from app.services.dummy_data import dummy_data_service

router = APIRouter()


# ===== VISITS ENDPOINTS =====


@router.get("/visits", response_model=FctVisitsListResponse)
def get_visits(
    db: Session = Depends(get_db_session),
    pagination: PaginationParams = Depends(get_pagination_params),
    search: Optional[str] = Query(
        None, description="Search in appkey, name, kunnr, address"
    ),
    empid: Optional[int] = Query(None, description="Employee ID filter"),
    code: Optional[str] = Query(None, description="Code filter"),
    kunnr: Optional[str] = Query(None, description="Customer number filter"),
    vtype: Optional[str] = Query(None, description="Visit type filter"),
    vdate_from: Optional[date] = Query(None, description="Visit date from"),
    vdate_to: Optional[date] = Query(None, description="Visit date to"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
) -> Any:
    """Get all visits with filtering and pagination"""

    # Calculate skip value
    skip = (pagination.page - 1) * pagination.size

    # Get visits with filters
    visits = fct_visits.get_multi_with_filters(
        db=db,
        skip=skip,
        limit=pagination.size,
        search=search,
        empid=empid,
        code=code,
        kunnr=kunnr,
        vtype=vtype,
        vdate_from=vdate_from,
        vdate_to=vdate_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    # Get total count
    total = fct_visits.get_count_with_filters(
        db=db,
        search=search,
        empid=empid,
        code=code,
        kunnr=kunnr,
        vtype=vtype,
        vdate_from=vdate_from,
        vdate_to=vdate_to,
    )

    return FctVisitsListResponse(
        items=visits, total=total, skip=skip, limit=pagination.size
    )


@router.get("/visits/{appkey}", response_model=FctVisitsResponse)
def get_visit(appkey: str, db: Session = Depends(get_db_session)) -> Any:
    """Get a specific visit by appkey"""
    visit = fct_visits.get_by_appkey(db=db, appkey=appkey)
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Visit with appkey {appkey} not found",
        )
    return visit


@router.post(
    "/visits", response_model=FctVisitsResponse, status_code=status.HTTP_201_CREATED
)
def create_visit(
    visit_in: FctVisitsCreate, db: Session = Depends(get_db_session)
) -> Any:
    """Create a new visit"""
    # Check if appkey already exists
    existing_visit = fct_visits.get_by_appkey(db=db, appkey=visit_in.appkey)
    if existing_visit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Visit with appkey {visit_in.appkey} already exists",
        )

    visit = fct_visits.create(db=db, obj_in=visit_in)
    return visit


@router.post("/visits/generate-dummy", response_model=List[FctVisitsResponse])
def generate_dummy_visits(
    count: int = Query(
        5, ge=1, le=50, description="Number of dummy visits to generate"
    ),
    db: Session = Depends(get_db_session),
) -> Any:
    """Generate dummy visit data for testing"""
    dummy_visits = dummy_data_service.generate_visits_dummy_data(count=count)
    created_visits = []

    for visit_data in dummy_visits:
        # Check if appkey exists, skip if it does
        existing = fct_visits.get_by_appkey(db=db, appkey=visit_data.appkey)
        if not existing:
            visit = fct_visits.create(db=db, obj_in=visit_data)
            created_visits.append(visit)

    return created_visits


# ===== SR HEADER ENDPOINTS =====


@router.get("/sr-headers", response_model=SrFctHeaderListResponse)
def get_sr_headers(
    db: Session = Depends(get_db_session),
    pagination: PaginationParams = Depends(get_pagination_params),
    search: Optional[str] = Query(
        None, description="Search in appkey, ship_name, kunnr, created_by"
    ),
    kunnr: Optional[str] = Query(None, description="Customer number filter"),
    code: Optional[str] = Query(None, description="Code filter"),
    fk_status: Optional[int] = Query(None, description="Status filter"),
    created_by: Optional[str] = Query(None, description="Created by filter"),
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
) -> Any:
    """Get all SR headers with filtering and pagination"""

    # Calculate skip value
    skip = (pagination.page - 1) * pagination.size

    # Get SR headers with filters
    headers = sr_fct_header.get_multi_with_filters(
        db=db,
        skip=skip,
        limit=pagination.size,
        search=search,
        kunnr=kunnr,
        code=code,
        fk_status=fk_status,
        created_by=created_by,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    # Get total count
    total = sr_fct_header.get_count_with_filters(
        db=db,
        search=search,
        kunnr=kunnr,
        code=code,
        fk_status=fk_status,
        created_by=created_by,
    )

    return SrFctHeaderListResponse(
        items=headers, total=total, skip=skip, limit=pagination.size
    )


@router.get("/sr-headers/{appkey}", response_model=SrFctHeaderDetailResponse)
def get_sr_header(
    appkey: str,
    db: Session = Depends(get_db_session),
    include_items: bool = Query(True, description="Include SR items in response"),
) -> Any:
    """Get a specific SR header by appkey with optional items"""
    header = sr_fct_header.get_by_appkey(db=db, appkey=appkey)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SR header with appkey {appkey} not found",
        )

    # If include_items is True, fetch items
    if include_items:
        items = sr_fct_items.get_by_appkey(db=db, appkey=appkey)
        # Add items to header object for response
        header.items = items

    return header


@router.post(
    "/sr-headers",
    response_model=SrFctHeaderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sr_header(
    header_in: SrFctHeaderCreate, db: Session = Depends(get_db_session)
) -> Any:
    """Create a new SR header"""
    # Check if appkey already exists
    existing_header = sr_fct_header.get_by_appkey(db=db, appkey=header_in.appkey)
    if existing_header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"SR header with appkey {header_in.appkey} already exists",
        )

    header = sr_fct_header.create(db=db, obj_in=header_in)
    return header


@router.post("/sr-headers/generate-dummy")
def generate_dummy_sr_headers(
    count: int = Query(
        3, ge=1, le=20, description="Number of dummy SR headers to generate"
    ),
    use_existing_visits: bool = Query(True, description="Use existing visit appkeys"),
    db: Session = Depends(get_db_session),
) -> Any:
    """Generate dummy SR header data for testing"""

    visit_appkeys = []
    if use_existing_visits:
        # Get some existing visit appkeys
        existing_visits = fct_visits.get_multi(db=db, skip=0, limit=10)
        visit_appkeys = [visit.appkey for visit in existing_visits]

    if not visit_appkeys:
        # Generate some visit appkeys if none exist
        visit_appkeys = [f"VIS{i:08d}" for i in range(1, count + 1)]

    dummy_headers = dummy_data_service.generate_sr_header_dummy_data(
        visit_appkeys=visit_appkeys, count=count
    )

    created_headers = []
    for header_data in dummy_headers:
        # Check if appkey exists, skip if it does
        existing = sr_fct_header.get_by_appkey(db=db, appkey=header_data.appkey)
        if not existing:
            header = sr_fct_header.create(db=db, obj_in=header_data)
            created_headers.append(header)

    return {
        "created_headers": created_headers,
        "count": len(created_headers),
        "message": f"Created {len(created_headers)} SR headers",
    }


# ===== SR ITEMS ENDPOINTS =====


@router.get("/sr-items", response_model=SrFctItemsListResponse)
def get_sr_items(
    db: Session = Depends(get_db_session),
    pagination: PaginationParams = Depends(get_pagination_params),
    appkey: Optional[str] = Query(None, description="Filter by SR header appkey"),
    matnr: Optional[str] = Query(None, description="Filter by material number"),
    fk_actiontype: Optional[int] = Query(None, description="Filter by action type"),
) -> Any:
    """Get all SR items with filtering and pagination"""

    # Calculate skip value
    skip = (pagination.page - 1) * pagination.size

    # Build filters
    filters = {}
    if appkey:
        filters["appkey"] = appkey
    if matnr:
        filters["matnr"] = matnr
    if fk_actiontype:
        filters["fk_actiontype"] = fk_actiontype

    # Get items
    items = sr_fct_items.get_multi(
        db=db, skip=skip, limit=pagination.size, filters=filters
    )

    # Get total count
    total = sr_fct_items.get_count(db=db, filters=filters)

    return SrFctItemsListResponse(
        items=items, total=total, skip=skip, limit=pagination.size
    )


@router.get("/sr-items/by-header/{appkey}", response_model=List[SrFctItemsResponse])
def get_sr_items_by_header(appkey: str, db: Session = Depends(get_db_session)) -> Any:
    """Get all items for a specific SR header"""
    items = sr_fct_items.get_by_appkey(db=db, appkey=appkey)
    return items


@router.post(
    "/sr-items", response_model=SrFctItemsResponse, status_code=status.HTTP_201_CREATED
)
def create_sr_item(
    item_in: SrFctItemsCreate, db: Session = Depends(get_db_session)
) -> Any:
    """Create a new SR item"""
    # Verify that the SR header exists
    header = sr_fct_header.get_by_appkey(db=db, appkey=item_in.appkey)
    if not header:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"SR header with appkey {item_in.appkey} not found",
        )

    item = sr_fct_items.create(db=db, obj_in=item_in)
    return item


@router.post("/sr-items/bulk", response_model=List[SrFctItemsResponse])
def create_sr_items_bulk(
    items_in: List[SrFctItemsCreate], db: Session = Depends(get_db_session)
) -> Any:
    """Create multiple SR items in bulk"""
    # Verify all appkeys exist
    unique_appkeys = list(set([item.appkey for item in items_in]))
    for appkey in unique_appkeys:
        header = sr_fct_header.get_by_appkey(db=db, appkey=appkey)
        if not header:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SR header with appkey {appkey} not found",
            )

    items = sr_fct_items.bulk_create(db=db, items=items_in)
    return items


@router.post("/sr-items/generate-dummy")
def generate_dummy_sr_items(
    items_per_header: int = Query(
        2, ge=1, le=10, description="Number of items per SR header"
    ),
    use_existing_headers: bool = Query(
        True, description="Use existing SR header appkeys"
    ),
    db: Session = Depends(get_db_session),
) -> Any:
    """Generate dummy SR items data for testing"""

    sr_appkeys = []
    if use_existing_headers:
        # Get existing SR header appkeys
        existing_headers = sr_fct_header.get_multi(db=db, skip=0, limit=10)
        sr_appkeys = [header.appkey for header in existing_headers]

    if not sr_appkeys:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No SR headers found. Please create SR headers first or set use_existing_headers=False",
        )

    dummy_items = dummy_data_service.generate_sr_items_dummy_data(
        sr_appkeys=sr_appkeys, items_per_header=items_per_header
    )

    created_items = sr_fct_items.bulk_create(db=db, items=dummy_items)

    return {
        "created_items": created_items,
        "count": len(created_items),
        "message": f"Created {len(created_items)} SR items for {len(sr_appkeys)} headers",
    }


# ===== COMBINED ENDPOINTS =====


@router.post("/generate-complete-dummy-dataset")
def generate_complete_dummy_dataset(
    visit_count: int = Query(
        5, ge=1, le=20, description="Number of visits to generate"
    ),
    sr_header_count: int = Query(
        3, ge=1, le=10, description="Number of SR headers to generate"
    ),
    items_per_header: int = Query(
        2, ge=1, le=5, description="Number of items per SR header"
    ),
    db: Session = Depends(get_db_session),
) -> Any:
    """Generate a complete dummy dataset with visits, SR headers, and items"""

    # Generate complete dataset
    dataset = dummy_data_service.create_complete_dummy_dataset(
        visit_count=visit_count,
        sr_header_count=sr_header_count,
        items_per_header=items_per_header,
    )

    created_visits = []
    created_headers = []
    created_items = []

    # Create visits
    for visit_data in dataset["visits"]:
        existing = fct_visits.get_by_appkey(db=db, appkey=visit_data.appkey)
        if not existing:
            visit = fct_visits.create(db=db, obj_in=visit_data)
            created_visits.append(visit)

    # Create SR headers
    for header_data in dataset["sr_headers"]:
        existing = sr_fct_header.get_by_appkey(db=db, appkey=header_data.appkey)
        if not existing:
            header = sr_fct_header.create(db=db, obj_in=header_data)
            created_headers.append(header)

    # Create SR items
    if dataset["sr_items"]:
        created_items = sr_fct_items.bulk_create(db=db, items=dataset["sr_items"])

    return {
        "visits": {"created": len(created_visits), "data": created_visits},
        "sr_headers": {"created": len(created_headers), "data": created_headers},
        "sr_items": {"created": len(created_items), "data": created_items},
        "summary": {
            "total_visits": len(created_visits),
            "total_sr_headers": len(created_headers),
            "total_sr_items": len(created_items),
            "message": "Complete dummy dataset created successfully",
        },
    }


@router.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db_session)) -> Any:
    """Get dashboard statistics"""

    # Get counts
    total_visits = fct_visits.get_count(db=db)
    total_sr_headers = sr_fct_header.get_count(db=db)
    total_sr_items = sr_fct_items.get_count(db=db)

    # Get recent visits
    recent_visits = fct_visits.get_recent_visits(db=db, days=7, limit=5)

    # Get recent SR headers
    recent_sr_headers = sr_fct_header.get_multi(db=db, skip=0, limit=5, filters=None)

    return {
        "totals": {
            "visits": total_visits,
            "sr_headers": total_sr_headers,
            "sr_items": total_sr_items,
        },
        "recent": {"visits": recent_visits, "sr_headers": recent_sr_headers},
    }
