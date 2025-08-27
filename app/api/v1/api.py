# app/api/v1/api.py
from fastapi import APIRouter

# Import only the essential SR routers
from app.api.v1.sr_header import router as sr_header_router
from app.api.v1.sr_items import router as sr_items_router
from app.api.v1.sr_attachment import router as sr_attachment_router
from app.api.v1.sr_sync import router as sr_sync_router

api_router = APIRouter()

# Include individual SR table routers (for debugging/admin purposes)
api_router.include_router(sr_header_router, prefix="/sr/headers", tags=["SR Headers"])
api_router.include_router(sr_items_router, prefix="/sr/items", tags=["SR Items"])
api_router.include_router(
    sr_attachment_router, prefix="/sr/attachments", tags=["SR Attachments"]
)

# Main sync router that provides the structured response
api_router.include_router(
    sr_sync_router, prefix="/sr/sync", tags=["SR Sync - Structured Data"]
)


@api_router.get("/")
async def api_root():
    return {"message": "API v1 is running"}
