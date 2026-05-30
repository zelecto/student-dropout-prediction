import sqlite3
from datetime import datetime
from pathlib import Path

from src.config import ROOT

DB_PATH = ROOT / "data" / "dropout.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sexo TEXT NOT NULL,
            edad INTEGER NOT NULL,
            promedio_general REAL NOT NULL,
            promedio_admision REAL,
            horas_tutoria REAL NOT NULL,
            ingreso_mensual REAL NOT NULL,
            materias_repetidas TEXT NOT NULL,
            ratio_aprobacion_sem1 REAL NOT NULL,
            ratio_aprobacion_sem2 REAL NOT NULL,
            trabaja TEXT NOT NULL,
            apoyo_familiar TEXT NOT NULL,
            responsabilidades_familiares TEXT NOT NULL,
            becado TEXT NOT NULL,
            matricula_al_dia TEXT NOT NULL,
            deudor TEXT NOT NULL,
            desplazado TEXT NOT NULL,
            tipo_vivienda TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predicciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL REFERENCES estudiantes(id),
            probabilidad_riesgo REAL NOT NULL,
            nivel_riesgo TEXT NOT NULL,
            desertó INTEGER NOT NULL,
            fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def crear_estudiante(data: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO estudiantes (
            sexo, edad, promedio_general, promedio_admision,
            horas_tutoria, ingreso_mensual, materias_repetidas,
            ratio_aprobacion_sem1, ratio_aprobacion_sem2,
            trabaja, apoyo_familiar, responsabilidades_familiares,
            becado, matricula_al_dia, deudor, desplazado, tipo_vivienda
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["sexo"], data["edad"], data["promedio_general"],
        data.get("promedio_admision", 7.0), data["horas_tutoria"],
        data["ingreso_mensual"], data["materias_repetidas"],
        data["ratio_aprobacion_sem1"], data["ratio_aprobacion_sem2"],
        data["trabaja"], data["apoyo_familiar"], data["responsabilidades_familiares"],
        data["becado"], data["matricula_al_dia"], data["deudor"],
        data["desplazado"], data["tipo_vivienda"]
    ))

    estudiante_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return estudiante_id


def guardar_prediccion(estudiante_id: int, probabilidad_riesgo: float, nivel_riesgo: str, desertó: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predicciones (estudiante_id, probabilidad_riesgo, nivel_riesgo, desertó)
        VALUES (?, ?, ?, ?)
    """, (estudiante_id, probabilidad_riesgo, nivel_riesgo, desertó))

    conn.commit()
    conn.close()


def get_indicadores_dashboard() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM estudiantes")
    total = cursor.fetchone()["total"]

    if total == 0:
        conn.close()
        return {
            "total_estudiantes": 0,
            "tasa_desercion": 0.0,
            "riesgo_alto": 0,
            "promedio_riesgo": 0.0,
            "por_genero": {
                "hombres": {"total": 0, "porcentaje": 0, "tasa_desercion": 0.0},
                "mujeres": {"total": 0, "porcentaje": 0, "tasa_desercion": 0.0}
            },
            "distribucion_riesgo": {"alto": 0, "medio": 0, "bajo": 0},
            "actualizado_el": datetime.now().isoformat()
        }

    cursor.execute("SELECT COUNT(*) as count FROM predicciones WHERE desertó = 1")
    desertaron = cursor.fetchone()["count"]
    tasa_desercion = round((desertaron / total) * 100, 1)

    cursor.execute("SELECT COUNT(*) as count FROM predicciones WHERE nivel_riesgo = 'Alto'")
    riesgo_alto = cursor.fetchone()["count"]

    cursor.execute("SELECT AVG(probabilidad_riesgo) as avg FROM predicciones")
    avg_result = cursor.fetchone()["avg"]
    promedio_riesgo = round(avg_result * 100, 1) if avg_result else 0.0

    cursor.execute("""
        SELECT sexo, COUNT(*) as total,
               SUM(CASE WHEN p.desertó = 1 THEN 1 ELSE 0 END) as desertores
        FROM estudiantes e
        JOIN predicciones p ON e.id = p.estudiante_id
        GROUP BY sexo
    """)
    resultados_genero = cursor.fetchall()

    por_genero = {"hombres": {"total": 0, "porcentaje": 0, "tasa_desercion": 0.0},
                  "mujeres": {"total": 0, "porcentaje": 0, "tasa_desercion": 0.0}}

    for row in resultados_genero:
        sexo = row["sexo"].lower()
        total_gen = row["total"]
        desertores = row["desertores"]
        porcentaje = round((total_gen / total) * 100, 0)
        tasa = round((desertores / total_gen) * 100, 1) if total_gen > 0 else 0.0

        if "hombre" in sexo or sexo == "m" or sexo == "h":
            por_genero["hombres"] = {"total": total_gen, "porcentaje": porcentaje, "tasa_desercion": tasa}
        else:
            por_genero["mujeres"] = {"total": total_gen, "porcentaje": porcentaje, "tasa_desercion": tasa}

    cursor.execute("""
        SELECT nivel_riesgo, COUNT(*) as count
        FROM predicciones
        GROUP BY nivel_riesgo
    """)
    resultados_riesgo = cursor.fetchall()

    distribucion_riesgo = {"alto": 0, "medio": 0, "bajo": 0}
    for row in resultados_riesgo:
        nivel = row["nivel_riesgo"].lower()
        if nivel == "alto":
            distribucion_riesgo["alto"] = row["count"]
        elif nivel == "medio":
            distribucion_riesgo["medio"] = row["count"]
        else:
            distribucion_riesgo["bajo"] = row["count"]

    conn.close()

    return {
        "total_estudiantes": total,
        "tasa_desercion": tasa_desercion,
        "riesgo_alto": riesgo_alto,
        "promedio_riesgo": promedio_riesgo,
        "por_genero": por_genero,
        "distribucion_riesgo": distribucion_riesgo,
        "actualizado_el": datetime.now().isoformat()
    }