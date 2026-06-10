import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import init_db, crear_estudiante, guardar_prediccion
from src.predict import clasificar_riesgo


# ── Datos ficticios para generación de nombres ──────────────────────────────
NOMBRES_M = [
    "Carlos", "Juan", "Miguel", "Andrés", "Luis", "Diego", "Santiago",
    "Sebastián", "Alejandro", "Mateo", "Daniel", "David", "Jorge",
    "Ricardo", "Fernando", "Cristian", "Camilo", "Jhon", "Esteban", "Manuel",
]
NOMBRES_F = [
    "María", "Valentina", "Daniela", "Camila", "Sofía", "Isabella", "Laura",
    "Natalia", "Alejandra", "Paula", "Juliana", "Sara", "Mariana", "Ana",
    "Lucía", "Diana", "Paola", "Catalina", "Adriana", "Karen",
]
APELLIDOS = [
    "García", "Martínez", "López", "Rodríguez", "González", "Pérez",
    "Hernández", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera",
    "Morales", "Jiménez", "Reyes", "Vargas", "Castillo", "Ramos",
    "Mendoza", "Ortiz", "Herrera", "Medina", "Aguilar", "Rojas",
    "Suárez", "Gutiérrez", "Cruz", "Rios", "Molina", "Moreno",
]


def generar_correo(nombres: str, apellidos: str, idx: int) -> str:
    """Genera un correo único basado en nombre, apellido e índice."""
    nombre_part = nombres.split()[0].lower()
    apellido_part = apellidos.split()[0].lower()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n")]:
        nombre_part = nombre_part.replace(a, b)
        apellido_part = apellido_part.replace(a, b)
    # El índice siempre va incluido → garantiza unicidad absoluta
    return f"{nombre_part}{idx}.{apellido_part}@universidad.edu.co"

def seed_dashboard():
    init_db()

    sexos = ["M", "F"]
    opciones_simple = ["Sí", "No"]
    tipos_vivienda = ["Propia", "Rentada", "Familiar", "Otro"]
    niveles_apoyo = ["Alto", "Medio", "Bajo", "Nulo"]

    total_target = 1250
    tasa_desercion_target = 30.4
    riesgo_alto_target = 380

    desertaron_target = int(total_target * tasa_desercion_target / 100)
    counts = {"M": 680, "F": 570}

    print(f"Generando {total_target} estudiantes mock...")

    desertaron_real = 0
    riesgo_alto_real = 0
    idx_global = 1  # Para garantizar correos únicos

    for sexo, count in counts.items():
        pool_nombres = NOMBRES_M if sexo == "M" else NOMBRES_F

        for _ in range(count):
            # ── Datos personales ────────────────────────────────────────────
            nombre1 = random.choice(pool_nombres)
            nombre2 = random.choice(pool_nombres)
            apellido1 = random.choice(APELLIDOS)
            apellido2 = random.choice(APELLIDOS)
            nombres = f"{nombre1} {nombre2}"
            apellidos = f"{apellido1} {apellido2}"
            correo = generar_correo(nombre1, apellido1, idx_global)
            idx_global += 1

            # ── Datos académicos y socioeconómicos ──────────────────────────
            edad = random.randint(16, 35)
            promedio_general = round(random.uniform(5.0, 10.0), 2)
            promedio_admision = round(random.uniform(6.0, 10.0), 2)
            horas_tutoria = round(random.uniform(0, 15), 1)
            ingreso_mensual = round(random.uniform(0, 3000), 2)

            ratio_sem1 = round(random.uniform(0.3, 1.0), 2)
            ratio_sem2 = round(random.uniform(0.3, 1.0), 2)

            materias_repetidas = random.choice(opciones_simple)
            trabaja = random.choice(opciones_simple)
            apoyo_familiar = random.choice(niveles_apoyo)
            responsabilidades_familiares = random.choice(opciones_simple)
            becado = random.choice(opciones_simple)
            matricula_al_dia = random.choice(opciones_simple)
            deudor = random.choice(opciones_simple)
            desplazado = random.choice(opciones_simple)
            tipo_vivienda = random.choice(tipos_vivienda)

            # ── Predicción ──────────────────────────────────────────────────
            if random.random() < 0.3:
                proba = random.uniform(0.6, 0.95)
            elif random.random() < 0.5:
                proba = random.uniform(0.3, 0.6)
            else:
                proba = random.uniform(0.0, 0.3)

            nivel = clasificar_riesgo(proba)
            desertó = 1 if nivel == "Alto" and desertaron_real < desertaron_target else 0

            if nivel == "Alto" and riesgo_alto_real < riesgo_alto_target:
                if random.random() < 0.7:
                    desertó = 1
                riesgo_alto_real += 1

            if desertó == 1:
                desertaron_real += 1

            # ── Persistencia ────────────────────────────────────────────────
            data = {
                "correo": correo,
                "nombres": nombres,
                "apellidos": apellidos,
                "sexo": sexo,
                "edad": edad,
                "promedio_general": promedio_general,
                "promedio_admision": promedio_admision,
                "horas_tutoria": horas_tutoria,
                "ingreso_mensual": ingreso_mensual,
                "materias_repetidas": materias_repetidas,
                "ratio_aprobacion_sem1": ratio_sem1,
                "ratio_aprobacion_sem2": ratio_sem2,
                "trabaja": trabaja,
                "apoyo_familiar": apoyo_familiar,
                "responsabilidades_familiares": responsabilidades_familiares,
                "becado": becado,
                "matricula_al_dia": matricula_al_dia,
                "deudor": deudor,
                "desplazado": desplazado,
                "tipo_vivienda": tipo_vivienda,
            }

            estudiante_id = crear_estudiante(data)
            guardar_prediccion(estudiante_id, proba, nivel, desertó)

    print(f"✓ {total_target} estudiantes creados")
    print(f"✓ Desertaron: {desertaron_real} ({round(desertaron_real/total_target*100, 1)}%)")
    print(f"✓ Riesgo alto: {riesgo_alto_real}")


if __name__ == "__main__":
    seed_dashboard()