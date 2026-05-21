from fastapi import APIRouter
from app.routers.business_profile_router import router as profile_router

# enrutador principal
api_router = APIRouter()

@api_router.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "service": "ms-CONFIGURATION"}

# Registrar Rutas
api_router.include_router(profile_router)