# app/api/v1/api.py
from fastapi import APIRouter

# Import your routers
from app.api.v1.sr_items import router as sr_items_router
from app.api.v1.sr_header import router as sr_header_router

api_router = APIRouter()

# Include the routers
api_router.include_router(
    sr_header_router, prefix="/sr/headers", tags=["Sales Return Headers"]
)
api_router.include_router(
    sr_items_router, prefix="/sr/items", tags=["Sales Return Items"]
)


@api_router.get("/")
async def api_root():
    return {"message": "API v1 is running"}
