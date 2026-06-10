from datetime import datetime, UTC

from fastapi import APIRouter, Depends, HTTPException, Request
import pandas as pd

from api.dependencies import get_model
from src.config import FEATURE_COLS
from src.database import (
    buscar_estudiante_por_correo,
    crear_estudiante_completo,
    crear_estudiante,
    guardar_prediccion,
    init_db,
)
from src.schemas import (
    StudentFeatures,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelInfo,
    RegistroPredictRequest,
    RegistroPredictResponse,
    EstudianteResponse,
)
from src.predict import clasificar_riesgo

router = APIRouter(prefix="/api/v1", tags=["Predicción"])


@router.post("/register-predict", response_model=RegistroPredictResponse)
async def register_and_predict(data: RegistroPredictRequest):
    from src.predict import load_model

    try:
        modelo, threshold = load_model()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Modelo no cargado. Ejecuta entrenamiento primero.")

    init_db()

    existente = buscar_estudiante_por_correo(data.correo)
    if existente:
        estudiante_id = existente["id"]
    else:
        data_dict = data.model_dump()
        estudiante_id = crear_estudiante_completo(data_dict)

    df = pd.DataFrame([data.model_dump()])
    proba = modelo.predict_proba(df[FEATURE_COLS])[:, 1][0]
    pred = int(proba >= threshold)
    nivel = clasificar_riesgo(proba)

    guardar_prediccion(estudiante_id, proba, nivel, pred)

    estudiante_response = EstudianteResponse(
        id=estudiante_id,
        correo=data.correo,
        nombres=data.nombres,
        apellidos=data.apellidos,
        fecha_registro=datetime.now(UTC).isoformat(),
    )

    return RegistroPredictResponse(
        estudiante=estudiante_response,
        riesgo=pred,
        probabilidad_riesgo=round(proba, 4),
        nivel_riesgo=nivel,
        timestamp=datetime.now(UTC),
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_single(
    student: StudentFeatures,
    model_data: tuple = Depends(get_model),
):
    modelo, threshold = model_data

    init_db()

    data = student.model_dump()
    estudiante_id = crear_estudiante_completo(data)

    df = pd.DataFrame([data])
    proba = modelo.predict_proba(df[FEATURE_COLS])[:, 1][0]
    pred = int(proba >= threshold)
    nivel = clasificar_riesgo(proba)

    guardar_prediccion(estudiante_id, proba, nivel, pred)

    return PredictionResponse(
        riesgo=pred,
        probabilidad_riesgo=round(proba, 4),
        nivel_riesgo=nivel,
        timestamp=datetime.now(UTC),
    )


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    batch: BatchPredictionRequest,
    model_data: tuple = Depends(get_model),
):
    modelo, threshold = model_data

    init_db()

    df = pd.DataFrame([s.model_dump() for s in batch.students])
    probas = modelo.predict_proba(df[FEATURE_COLS])[:, 1]

    predictions = []
    for i, proba in enumerate(probas):
        data = batch.students[i].model_dump()
        estudiante_id = crear_estudiante(data)  # tolera correo/nombres/apellidos opcionales

        pred = int(proba >= threshold)
        nivel = clasificar_riesgo(proba)

        guardar_prediccion(estudiante_id, proba, nivel, pred)

        predictions.append(PredictionResponse(
            riesgo=pred,
            probabilidad_riesgo=round(proba, 4),
            nivel_riesgo=nivel,
            timestamp=datetime.now(UTC),
        ))

    return BatchPredictionResponse(predictions=predictions, total=len(predictions))


@router.get("/model/info", response_model=ModelInfo)
async def model_info(request: Request):
    return ModelInfo(
        features=FEATURE_COLS,
        threshold=getattr(request.app.state, "threshold", 0.5),
        loaded_at=getattr(request.app.state, "model_loaded_at", None),
    )