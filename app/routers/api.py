from fastapi import APIRouter

<<<<<<< HEAD
from app.routers.business_profile_router import router as profile_router
=======
#enrutador
api_router=APIRouter(prefix="/api/v1/configuration")

@api_router.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "service": "ms-CONFIGURATION"}
>>>>>>> c4787cf112f872d6ebe60e1437d516b9ef967aac

# enrutador principal
api_router = APIRouter()

# Registrar Rutas
api_router.include_router(profile_router)