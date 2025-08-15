from fastapi import APIRouter

# Import your endpoint routers here as you create them
# from app.api.v1.endpoints import sr_headers, customers, materials

api_router = APIRouter()

# Include endpoint routers here as you create them
# api_router.include_router(sr_headers.router, prefix="/sr-headers", tags=["sr-headers"])
# api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
# api_router.include_router(materials.router, prefix="/materials", tags=["materials"])


@api_router.get("/")
async def api_root():
    return {"message": "API v1 is running"}
