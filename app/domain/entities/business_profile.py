class BusinessProfile:
    def __init__(
        self,
        nombre_perfil,
        peso_poblacion,
        peso_ingresos,
        peso_competencia,
        is_active=True
    ):
        self.nombre_perfil = nombre_perfil
        self.peso_poblacion = peso_poblacion
        self.peso_ingresos = peso_ingresos
        self.peso_competencia = peso_competencia
        self.is_active = is_active

    def suma_pesos(self):
        return round(
            self.peso_poblacion +
            self.peso_ingresos +
            self.peso_competencia, 2
        )

    def es_valido(self):
        return self.suma_pesos() == 1.0
    
    #✔ Validación de suma = 1
#✔ Entidad de negocio