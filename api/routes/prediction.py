from datetime import datetime, UTC

from fastapi import APIRouter, Depends, Request
import pandas as pd

from api.dependencies import get_model
from src.config import FEATURE_COLS
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

    df = pd.DataFrame([student.model_dump()])
    proba = modelo.predict_proba(df[FEATURE_COLS])[:, 1][0]
    pred = int(proba >= threshold)

    return PredictionResponse(
        riesgo=pred,
        probabilidad_riesgo=round(proba, 4),
        nivel_riesgo=clasificar_riesgo(proba),
        timestamp=datetime.now(UTC),
    )


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    batch: BatchPredictionRequest,
    model_data: tuple = Depends(get_model),
):
    modelo, threshold = model_data

    df = pd.DataFrame([s.model_dump() for s in batch.students])
    probas = modelo.predict_proba(df[FEATURE_COLS])[:, 1]

    predictions = []
    for proba in probas:
        predictions.append(PredictionResponse(
            riesgo=int(proba >= threshold),
            probabilidad_riesgo=round(proba, 4),
            nivel_riesgo=clasificar_riesgo(proba),
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
