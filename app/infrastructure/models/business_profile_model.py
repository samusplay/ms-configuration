from sqlalchemy import Column, Integer, String, Float, Boolean
from app.infrastructure.database import Base

class BusinessProfileModel(Base):
    __tablename__ = "business_profiles"

    id = Column(Integer, primary_key=True, index=True)
    nombre_perfil = Column(String, nullable=False)

    peso_poblacion = Column(Float, nullable=False)
    peso_ingresos = Column(Float, nullable=False)
    peso_competencia = Column(Float, nullable=False)

    is_active = Column(Boolean, default=True)