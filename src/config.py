from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
MODELS_DIR = ROOT / "models"

DATASET_FINAL = PROCESSED_DIR / "dataset_final_ia.csv"
MODEL_PATH = MODELS_DIR / "modelo_rf.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2

CATEGORICAL_COLS = [
    "sexo",
    "materias_repetidas",
    "trabaja",
    "apoyo_familiar",
    "responsabilidades_familiares",
    "becado",
    "matricula_al_dia",
    "deudor",
    "desplazado",
    "tipo_vivienda",
]

NUMERICAL_COLS = [
    "edad",
    "promedio_general",
    "horas_tutoria",
    "ingreso_mensual",
    "ratio_aprobacion_sem1",
    "ratio_aprobacion_sem2",
]

FEATURE_COLS = CATEGORICAL_COLS + NUMERICAL_COLS
TARGET_COL = "target"

MODEL_PARAMS = {
    "n_estimators": 300,
    "max_depth": 12,
    "min_samples_split": 10,
    "min_samples_leaf": 4,
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
    "class_weight": "balanced",
}

RF_PARAM_GRID = {
    "classifier__n_estimators": [100, 200, 300],
    "classifier__max_depth": [8, 12, 16, None],
    "classifier__min_samples_split": [5, 10, 15],
    "classifier__min_samples_leaf": [2, 4, 6],
}
