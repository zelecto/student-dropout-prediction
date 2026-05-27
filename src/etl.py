# =========================================================
# STUDENT-DROPOUT-PREDICTION
# ETL — Carga, limpieza y unificación de datasets
# =========================================================

import pandas as pd
import numpy as np
from pathlib import Path

# Rutas base
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"


# =========================================================
# CONSTANTES
# =========================================================

RENAME_UPC = {
    "Edad del estudiante": "edad",
    "Sexo del estudiante": "sexo",
    "Ha repetido alguna materia": "materias_repetidas",
    "Horas de tutoría al mes": "horas_tutoria",
    "Trabaja mientras estudia": "trabaja",
    "c_ing_gen": "ingreso_mensual",
    "cuan_ap_f": "apoyo_familiar",
    "Responsabilidades familiares": "responsabilidades_familiares",
    "Promedio académico último semestre": "promedio_general",
    "Tipo de vivienda": "tipo_vivienda",
    "retirarse": "target",
}

RENAME_INT = {
    "Age at enrollment": "edad",
    "Gender": "sexo",
    "Scholarship holder": "becado",
    "Debtor": "deudor",
    "Tuition fees up to date": "matricula_al_dia",
    "Displaced": "desplazado",
    "Curricular units 1st sem (approved)": "aprobadas_sem1",
    "Curricular units 2nd sem (approved)": "aprobadas_sem2",
    "Curricular units 1st sem (enrolled)": "matriculadas_sem1",
    "Curricular units 2nd sem (enrolled)": "matriculadas_sem2",
    "Curricular units 1st sem (grade)": "promedio_sem1",
    "Curricular units 2nd sem (grade)": "promedio_sem2",
    "Target": "target",
}

VARIABLES_FINALES = [
    "edad",
    "sexo",
    "promedio_general",
    "materias_repetidas",
    "horas_tutoria",
    "trabaja",
    "ingreso_mensual",
    "apoyo_familiar",
    "responsabilidades_familiares",
    "becado",
    "matricula_al_dia",
    "deudor",
    "desplazado",
    "tipo_vivienda",
    "ratio_aprobacion_sem1",
    "ratio_aprobacion_sem2",
    "target",
]


# =========================================================
# FUNCIONES
# =========================================================

def cargar_upc() -> pd.DataFrame:
    """Carga y transforma el dataset UPC (encuesta local)."""
    path = RAW_DIR / "ENCUESTA_UPECISTA (200 datos).xlsx"
    df = pd.read_excel(path)
    df.rename(columns=RENAME_UPC, inplace=True)
    df["target"] = df["target"].astype(int)
    print(f"[UPC] {len(df)} registros cargados")
    return df


def cargar_internacional() -> pd.DataFrame:
    """Carga y transforma el dataset internacional."""
    path = RAW_DIR / "dataset_internacional.csv"
    df = pd.read_csv(path)
    df.rename(columns=RENAME_INT, inplace=True)

    # Normalizar target
    df["target"] = df["target"].replace({
        "Graduate": 0,
        "Dropout": 1,
        "Enrolled": 0,
    })

    # Feature engineering
    df["ratio_aprobacion_sem1"] = (
        df["aprobadas_sem1"] / df["matriculadas_sem1"]
    )
    df["ratio_aprobacion_sem2"] = (
        df["aprobadas_sem2"] / df["matriculadas_sem2"]
    )
    df["promedio_general"] = (
        df["promedio_sem1"] + df["promedio_sem2"]
    ) / 2

    print(f"[INT] {len(df)} registros cargados")
    return df


def homologar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas faltantes como NaN y filtra las variables finales."""
    for col in VARIABLES_FINALES:
        if col not in df.columns:
            df[col] = np.nan
    return df[VARIABLES_FINALES]


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Reemplaza infinitos, elimina duplicados y rellena nulos con la mediana."""
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.drop_duplicates()

    numericas = df.select_dtypes(include=["int64", "float64"]).columns
    for col in numericas:
        df[col] = df[col].fillna(df[col].median())

    return df


def run_etl() -> pd.DataFrame:
    """Ejecuta el pipeline ETL completo y exporta el dataset final."""
    print("=" * 50)
    print("INICIANDO ETL")
    print("=" * 50)

    df_upc = homologar_columnas(cargar_upc())
    df_int = homologar_columnas(cargar_internacional())

    df_final = pd.concat([df_upc, df_int], ignore_index=True)
    df_final = limpiar(df_final)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "dataset_final_ia.csv"
    df_final.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 50)
    print("DATASET FINAL GENERADO")
    print("=" * 50)
    print(f"Registros  : {df_final.shape[0]}")
    print(f"Columnas   : {df_final.shape[1]}")
    print(f"Exportado  : {output_path}")
    print("\nDistribución Target:")
    print(df_final["target"].value_counts().to_string())

    return df_final
