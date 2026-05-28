from datetime import datetime
from pydantic import BaseModel, Field

from src.config import FEATURE_COLS


class StudentFeatures(BaseModel):
    edad: int = Field(ge=0, description="Edad del estudiante")
    sexo: str = Field(description="Sexo (M/F)")
    promedio_general: float = Field(ge=0)
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


class PredictionResponse(PredictionResult):
    timestamp: datetime


class BatchPredictionRequest(BaseModel):
    students: list[StudentFeatures]


class BatchPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
    total: int


class ModelInfo(BaseModel):
    features: list[str]
    threshold: float
    loaded_at: datetime | None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_info: ModelInfo | None = None
