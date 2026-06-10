from datetime import datetime
from pydantic import BaseModel, Field

from src.config import FEATURE_COLS


class LoginRequest(BaseModel):
    correo: str = Field(description="Correo electrónico del estudiante")
    contraseña: str = Field(description="Contraseña del estudiante")


class RegistroPredictRequest(BaseModel):
    nombres: str = Field(min_length=1, max_length=100, description="Nombres del estudiante")
    apellidos: str = Field(min_length=1, max_length=100, description="Apellidos del estudiante")
    correo: str = Field(description="Correo electrónico del estudiante")
    edad: int = Field(ge=15, le=60, description="Edad del estudiante")
    sexo: str = Field(description="Sexo (M/F)")
    promedio_general: float = Field(ge=0)
    promedio_admision: float | None = Field(default=None, description="Promedio de admisión")
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


class EstudianteResponse(BaseModel):
    id: int
    correo: str
    nombres: str
    apellidos: str
    fecha_registro: str


class RegistroPredictResponse(BaseModel):
    estudiante: EstudianteResponse
    riesgo: int = Field(description="1 = Riesgo de abandono, 0 = Continúa")
    probabilidad_riesgo: float = Field(ge=0, le=1)
    nivel_riesgo: str = Field(description="Bajo / Medio / Alto")
    timestamp: datetime


class PrediccionItem(BaseModel):
    id: int
    probabilidad_riesgo: float
    nivel_riesgo: str
    desertó: int
    fecha_prediccion: str


class HistorialEstudianteResponse(BaseModel):
    id: int
    correo: str
    nombres: str
    apellidos: str
    sexo: str
    edad: int
    fecha_registro: str
    predicciones: list[PrediccionItem]


class PaginatedEstudiantesResponse(BaseModel):
    data: list[dict]
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int

class Admon (BaseModel):
    correo: str = Field(description="Correo electrónico del administrador")
    contraseña: str = Field(description="Contraseña del administrador")
    Nombre: str = Field(description="Nombre del administrador")
    Apellido: str = Field(description="Apellido del administrador")

class StudentFeatures(BaseModel):
    correo: str | None = None
    nombres: str | None = None
    apellidos: str | None = None
    edad: int = Field(ge=0, description="Edad del estudiante")
    sexo: str = Field(description="Sexo (M/F)")
    promedio_general: float = Field(ge=0)
    promedio_admision: float | None = Field(default=None, description="Promedio de admisión")
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


class GeneroStats(BaseModel):
    total: int
    porcentaje: float
    tasa_desercion: float


class DashboardResponse(BaseModel):
    total_estudiantes: int
    tasa_desercion: float
    riesgo_alto: int
    promedio_riesgo: float
    por_genero: dict[str, GeneroStats]
    distribucion_riesgo: dict[str, int]
    actualizado_el: datetime