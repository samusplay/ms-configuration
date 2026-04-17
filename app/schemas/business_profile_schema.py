from pydantic import BaseModel

class BusinessProfileCreate(BaseModel):
    nombre_perfil: str
    peso_poblacion: float
    peso_ingresos: float
    peso_competencia: float
    is_active: bool = True


class BusinessProfileResponse(BusinessProfileCreate):
    id: int

    class Config:
        orm_mode = True