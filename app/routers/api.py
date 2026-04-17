from fastapi import APIRouter

#enrutador
api_router=APIRouter(prefix="/api/v1/configuration")

@api_router.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "service": "ms-CONFIGURATION"}

#Registrar Rutas