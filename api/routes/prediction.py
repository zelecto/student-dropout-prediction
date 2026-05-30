from datetime import datetime, UTC

from fastapi import APIRouter, Depends, Request
import pandas as pd

from api.dependencies import get_model
from src.config import FEATURE_COLS
from src.database import crear_estudiante, guardar_prediccion, init_db
from src.schemas import (
    StudentFeatures,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    ModelInfo,
)
from src.predict import clasificar_riesgo

router = APIRouter(prefix="/api/v1", tags=["Predicción"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_single(
    student: StudentFeatures,
    model_data: tuple = Depends(get_model),
):
    modelo, threshold = model_data

    init_db()

    data = student.model_dump()
    estudiante_id = crear_estudiante(data)

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
        estudiante_id = crear_estudiante(data)

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