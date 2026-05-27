import warnings

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
    f1_score,
)

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

from src.config import (
    DATASET_FINAL,
    MODEL_PATH,
    MODELS_DIR,
    CATEGORICAL_COLS,
    NUMERICAL_COLS,
    FEATURE_COLS,
    TARGET_COL,
    RANDOM_STATE,
    MODEL_PARAMS,
    RF_PARAM_GRID,
)


def cargar_dataset(path: str | None = None) -> pd.DataFrame:
    path = path or DATASET_FINAL
    df = pd.read_csv(path)
    print(f"[DATASET] {len(df)} registros, {len(df.columns)} columnas")
    return df


def preparar_datos(df: pd.DataFrame, test_size: float = 0.2):
    X = df[FEATURE_COLS].copy()
    y = df[TARGET_COL].copy()

    for col in CATEGORICAL_COLS:
        X[col] = X[col].astype(object)
    for col in NUMERICAL_COLS:
        X[col] = pd.to_numeric(X[col], errors="coerce").astype(float)

    if test_size > 0:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
        )
        print(f"[TRAIN] {len(X_train)} muestras")
        print(f"[TEST]  {len(X_test)} muestras")
        print(f"[TARGET] 0={sum(y==0)}, 1={sum(y==1)}")
        return X_train, X_test, y_train, y_test

    print(f"[FULL] {len(X)} muestras")
    return X, None, y, None


def construir_pipeline() -> Pipeline:
    preprocessor = ColumnTransformer([
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
        ]), CATEGORICAL_COLS),
        ("num", SimpleImputer(strategy="median"), NUMERICAL_COLS),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(**MODEL_PARAMS)),
    ])

    return pipeline


def entrenar(pipeline: Pipeline, X_train, y_train, optimizar: bool = True):
    if optimizar:
        print("[HPO] Buscando hiperparámetros...")
        search = RandomizedSearchCV(
            pipeline,
            RF_PARAM_GRID,
            n_iter=15,
            cv=5,
            scoring="roc_auc",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        search.fit(X_train, y_train)
        print(f"[HPO] Mejores parámetros:\n{search.best_params_}")
        return search.best_estimator_

    pipeline.fit(X_train, y_train)
    return pipeline


def evaluar(modelo: Pipeline, X_test, y_test, threshold: float = 0.5, titulo: str = "EVALUACIÓN DEL MODELO"):
    y_proba = modelo.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    print(f"\n{'=' * 50}")
    print(f"{titulo} (threshold={threshold:.2f})")
    print(f"{'=' * 50}")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC  : {roc_auc_score(y_test, y_proba):.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "threshold": threshold,
    }


def optimizar_umbral(y_true, y_proba, min_precision: float = 0.70) -> float:
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_proba)
    mask = precisions[:-1] >= min_precision
    if mask.any():
        valid_idx = np.where(mask)[0]
        best_idx = valid_idx[np.argmax(recalls[valid_idx])]
    else:
        best_idx = np.argmax(recalls[:-1])
    best_threshold = thresholds[best_idx]
    print(f"\n[UMBRAL] Threshold={best_threshold:.4f} "
          f"(recall={recalls[best_idx]:.4f}, precision={precisions[best_idx]:.4f})")
    return best_threshold


def mostrar_importancia(modelo: Pipeline):
    rf = modelo.named_steps["classifier"]
    preprocessor = modelo.named_steps["preprocessor"]

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        feature_names = FEATURE_COLS[: len(rf.feature_importances_)]

    importancias = pd.DataFrame({
        "feature": feature_names,
        "importance": rf.feature_importances_,
    }).sort_values("importance", ascending=False)

    print(f"\n{'=' * 50}")
    print("IMPORTANCIA DE VARIABLES")
    print(f"{'=' * 50}")
    print(importancias.to_string(index=False))
    return importancias


def guardar_modelo(modelo: Pipeline, threshold: float = 0.5):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump({"modelo": modelo, "threshold": threshold}, MODEL_PATH)
    print(f"\n[MODELO] Guardado en: {MODEL_PATH} (threshold={threshold:.2f})")


def run_training(path: str | None = None, optimizar: bool = True):
    print(f"\n{'=' * 50}")
    print("ENTRENAMIENTO DEL MODELO")
    print(f"{'=' * 50}")

    df = cargar_dataset(path)
    X_train, X_test, y_train, y_test = preparar_datos(df, test_size=0.2)

    pipeline = construir_pipeline()
    modelo = entrenar(pipeline, X_train, y_train, optimizar=optimizar)

    metricas = evaluar(modelo, X_test, y_test, threshold=0.5, titulo="EVALUACIÓN (test set, threshold=0.5)")

    y_proba_test = modelo.predict_proba(X_test)[:, 1]
    best_threshold = optimizar_umbral(y_test, y_proba_test)
    metricas_opt = evaluar(modelo, X_test, y_test, threshold=best_threshold, titulo="EVALUACIÓN (test set, threshold óptimo)")

    mostrar_importancia(modelo)

    print(f"\n{'=' * 50}")
    print("ENTRENANDO MODELO FINAL CON TODOS LOS DATOS")
    print(f"{'=' * 50}")
    X_all, _, y_all, _ = preparar_datos(df, test_size=0)
    pipeline_final = construir_pipeline()
    pipeline_final.fit(X_all, y_all)
    evaluar(pipeline_final, X_all, y_all, threshold=best_threshold, titulo="EVALUACIÓN FINAL (todos los datos)")

    guardar_modelo(pipeline_final, threshold=best_threshold)

    return pipeline_final, metricas_opt
