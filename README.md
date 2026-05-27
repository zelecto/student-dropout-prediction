# Student Dropout Prediction

Predicción de deserción estudiantil combinando datos de encuestas UPC con un dataset internacional.

## Estructura del proyecto

```
student-dropout-prediction/
├── data/
│   ├── raw/               # Datos originales (Excel + CSV)
│   └── processed/         # Dataset limpio listo para el modelo
├── models/                # Modelos entrenados (.pkl)
├── src/
│   ├── config.py          # Configuración centralizada (rutas, columnas, hiperparámetros)
│   ├── etl.py             # Pipeline ETL: carga, limpieza y unificación
│   ├── train.py           # Entrenamiento del modelo (Random Forest)
│   ├── predict.py         # Inferencia con modelo entrenado
│   └── schemas.py         # Schemas Pydantic (prepara API)
├── api/                   # Futura implementación FastAPI
│   └── routes.py          # Rutas stub para FastAPI
├── notebooks/             # Exploración y análisis (Jupyter)
├── main.py                # Punto de entrada CLI
├── requirements.txt
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Solo ETL (generar dataset limpio)

```bash
python main.py
```

### ETL + Entrenamiento del modelo

```bash
python main.py --train
```

### ETL + Entrenamiento sin optimización de hiperparámetros

```bash
python main.py --train --no-optimize
```

### Predicción con modelo entrenado

```python
from src.predict import load_model, predecir_estudiante
import pandas as pd

modelo = load_model()
datos = pd.DataFrame([{...}])
resultados = predecir_estudiante(modelo, datos)
```

## Pipeline

1. **ETL** → `data/processed/dataset_final_ia.csv`
2. **Train** → `models/modelo_rf.pkl` + métricas de evaluación
3. **Predict** → Carga el modelo y genera predicciones con probabilidad y nivel de riesgo

## Variables del modelo

| Variable | Descripción |
|---|---|
| `edad` | Edad del estudiante |
| `sexo` | Sexo |
| `promedio_general` | Promedio académico |
| `materias_repetidas` | Si ha repetido materias |
| `horas_tutoria` | Horas de tutoría al mes |
| `trabaja` | Si trabaja mientras estudia |
| `ingreso_mensual` | Ingreso mensual familiar |
| `apoyo_familiar` | Nivel de apoyo familiar |
| `responsabilidades_familiares` | Responsabilidades en el hogar |
| `becado` | Si tiene beca |
| `matricula_al_dia` | Si la matrícula está al día |
| `deudor` | Si tiene deudas |
| `desplazado` | Si es estudiante desplazado |
| `tipo_vivienda` | Tipo de vivienda |
| `ratio_aprobacion_sem1` | Ratio aprobación semestre 1 |
| `ratio_aprobacion_sem2` | Ratio aprobación semestre 2 |
| `target` | 1 = Desertor, 0 = Continúa |
