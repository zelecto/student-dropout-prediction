import logging
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from src.config import MODEL_PATH, FEATURE_COLS

logger = logging.getLogger(__name__)


def load_model(path: str | Path | None = None) -> tuple:
    path = path or MODEL_PATH
    if not Path(path).exists():
        raise FileNotFoundError(f"Modelo no encontrado: {path}. Ejecuta entrenamiento primero.")
    data = joblib.load(path)
    if isinstance(data, dict):
        modelo = data["modelo"]
        threshold = data.get("threshold", 0.5)
    else:
        modelo = data
        threshold = 0.5
    logger.info(f"[MODELO] Cargado desde: {path} (threshold={threshold:.2f})")
    return modelo, threshold


def predict(modelo, datos: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
    X = datos[FEATURE_COLS] if all(c in datos.columns for c in FEATURE_COLS) else datos
    proba = modelo.predict_proba(X)[:, 1]
    return (proba >= threshold).astype(int)


def predict_proba(modelo, datos: pd.DataFrame) -> np.ndarray:
    X = datos[FEATURE_COLS] if all(c in datos.columns for c in FEATURE_COLS) else datos
    return modelo.predict_proba(X)[:, 1]


def clasificar_riesgo(probabilidad: float) -> str:
    if probabilidad < 0.3:
        return "Bajo"
    elif probabilidad < 0.6:
        return "Medio"
    return "Alto"


def ajustar_probabilidad(data: dict, proba: float) -> float:
    promedio = data.get("promedio_general", 0) or 0
    ingreso = data.get("ingreso_mensual", 0) or 0
    ratio_sem1 = data.get("ratio_aprobacion_sem1", 0) or 0
    ratio_sem2 = data.get("ratio_aprobacion_sem2", 0) or 0
    ratio_prom = (ratio_sem1 + ratio_sem2) / 2

    if promedio >= 15 and ingreso >= 1000000 and ratio_prom >= 0.85:
        ajuste = 0.35
        return round(proba * ajuste, 4)
    return proba


def predecir_estudiante(
    modelo, datos: pd.DataFrame, threshold: float = 0.5, detallado: bool = True
) -> pd.DataFrame:
    probas = predict_proba(modelo, datos)
    preds = (probas >= threshold).astype(int)

    resultados = datos.copy()
    resultados["prediccion"] = preds
    resultados["probabilidad_riesgo"] = probas.round(4)
    resultados["nivel_riesgo"] = resultados["probabilidad_riesgo"].apply(clasificar_riesgo)

    logger.info(f"Predicción completada: {len(resultados)} registros")

    return resultados
