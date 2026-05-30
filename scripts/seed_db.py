import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import init_db, crear_estudiante, guardar_prediccion
from src.predict import clasificar_riesgo


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

    for sexo, count in counts.items():
        for _ in range(count):
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

            data = {
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