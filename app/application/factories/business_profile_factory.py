from app.domain.entities.business_profile import BusinessProfile

class BusinessProfileFactory:

    @staticmethod
    def create_profile(data: dict) -> BusinessProfile:
        profile = BusinessProfile(
            nombre_perfil=data["nombre_perfil"],
            peso_poblacion=data["peso_poblacion"],
            peso_ingresos=data["peso_ingresos"],
            peso_competencia=data["peso_competencia"],
            is_active=data.get("is_active", True)
        )

        # 🔥 VALIDACIÓN CLAVE (historia funcional)
        if not profile.es_valido():
            raise ValueError("La suma de los pesos debe ser igual a 1.0")

        return profile