# app/api/v1/api.py
from fastapi import APIRouter

# Import your router
# from app.api.v1.salesreturn import router as salesreturn_router
from app.api.v1.sr_items import router as sr_items_router

# Import your endpoint routers here as you create them

api_router = APIRouter()

# Include the sr_management router
# api_router.include_router(salesreturn_router, prefix="/sr", tags=["Sales Return"])
api_router.include_router(sr_items_router, prefix="/sr/items", tags=["Sales Return Items"])


@api_router.get("/")
async def api_root():
    return {"message": "API v1 is running"}
