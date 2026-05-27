from pydantic import BaseModel, Field


class StudentFeatures(BaseModel):
    edad: int = Field(ge=15, le=99, description="Edad del estudiante")
    sexo: str = Field(description="Sexo (M/F)")
    promedio_general: float = Field(ge=0, le=20)
    materias_repetidas: str = Field(description="Ha repetido materias (Sí/No)")
    horas_tutoria: float = Field(ge=0)
    trabaja: str = Field(description="Trabaja mientras estudia (Sí/No)")
    ingreso_mensual: float = Field(ge=0)
    apoyo_familiar: str = Field(description="Nivel de apoyo familiar")
    responsabilidades_familiares: str = Field(description="Responsabilidades del hogar")
    becado: str = Field(description="Tiene beca (Sí/No)")
    matricula_al_dia: str = Field(description="Matrícula al día (Sí/No)")
    deudor: str = Field(description="Posee deuda (Sí/No)")
    desplazado: str = Field(description="Desplazado (Sí/No)")
    tipo_vivienda: str = Field(description="Tipo de vivienda")
    ratio_aprobacion_sem1: float = Field(ge=0, le=1)
    ratio_aprobacion_sem2: float = Field(ge=0, le=1)


class PredictionResult(BaseModel):
    riesgo: int = Field(description="1 = Riesgo de abandono, 0 = Continúa")
    probabilidad_riesgo: float = Field(ge=0, le=1)
    nivel_riesgo: str = Field(description="Bajo / Medio / Alto")
