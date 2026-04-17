from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.models.business_profile_model import BusinessProfileModel
from app.application.factories.business_profile_factory import BusinessProfileFactory
from app.schemas.business_profile_schema import BusinessProfileCreate, BusinessProfileResponse

router = APIRouter(prefix="/api/v1/profiles", tags=["Business Profiles"])


@router.post("/", response_model=BusinessProfileResponse)
def create_profile(data: BusinessProfileCreate, db: Session = Depends(get_db)):
    try:
        # 🔥 Validación con Factory
        profile = BusinessProfileFactory.create_profile(data.dict())

        # Guardar en DB
        db_profile = BusinessProfileModel(
            nombre_perfil=profile.nombre_perfil,
            peso_poblacion=profile.peso_poblacion,
            peso_ingresos=profile.peso_ingresos,
            peso_competencia=profile.peso_competencia,
            is_active=profile.is_active
        )

        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)

        return db_profile

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[BusinessProfileResponse])
def get_profiles(db: Session = Depends(get_db)):
    return db.query(BusinessProfileModel).all()
@router.put("/{profile_id}", response_model=BusinessProfileResponse)
def update_profile(profile_id: int, data: BusinessProfileCreate, db: Session = Depends(get_db)):
    # Buscar perfil existente
    db_profile = db.query(BusinessProfileModel).filter(BusinessProfileModel.id == profile_id).first()

    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")

    try:
        # Validar con Factory
        profile = BusinessProfileFactory.create_profile(data.dict())

        # Actualizar campos
        db_profile.nombre_perfil = profile.nombre_perfil
        db_profile.peso_poblacion = profile.peso_poblacion
        db_profile.peso_ingresos = profile.peso_ingresos
        db_profile.peso_competencia = profile.peso_competencia
        db_profile.is_active = profile.is_active

        db.commit()
        db.refresh(db_profile)

        return db_profile

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))