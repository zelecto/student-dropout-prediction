# API Documentation — Student Dropout Prediction

Base URL: `http://localhost:8000`

---

## Endpoints

### 1. Health Check

```
GET /health
```

**Response** `200 OK`
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_info": {
    "features": [],
    "threshold": 0.45,
    "loaded_at": "2026-05-28T19:31:47.363866Z"
  }
}
```

| status | Significado |
|---|---|
| `ok` | API y modelo operativos |
| `degraded` | API funciona pero modelo no cargado |

---

### 2. Model Info

```
GET /api/v1/model/info
```

**Response** `200 OK`
```json
{
  "features": [
    "sexo", "materias_repetidas", "trabaja", "apoyo_familiar",
    "responsabilidades_familiares", "becado", "matricula_al_dia",
    "deudor", "desplazado", "tipo_vivienda",
    "edad", "promedio_general", "horas_tutoria",
    "ingreso_mensual", "ratio_aprobacion_sem1", "ratio_aprobacion_sem2"
  ],
  "threshold": 0.4514,
  "loaded_at": "2026-05-28T19:31:47.363866Z"
}
```

---

### 3. Predict Single Student

```
POST /api/v1/predict
Content-Type: application/json
```

**Request Body** — `StudentFeatures`

| Campo | Tipo | Requerido | Descripción |
|---|---|---|---|
| `edad` | `int` | Sí | Edad (>= 0) |
| `sexo` | `str` | Sí | "M" / "F" |
| `promedio_general` | `float` | Sí | Promedio académico (>= 0) |
| `materias_repetidas` | `str` | Sí | "Sí" / "No" |
| `horas_tutoria` | `float` | Sí | Horas de tutoría al mes (>= 0) |
| `trabaja` | `str` | Sí | "Sí" / "No" |
| `ingreso_mensual` | `float` | Sí | Ingreso mensual familiar (>= 0) |
| `apoyo_familiar` | `str` | Sí | Nivel: "Alto" / "Medio" / "Bajo" |
| `responsabilidades_familiares` | `str` | Sí | "Bajo" / "Medio" / "Alto" |
| `becado` | `str` | Sí | "Sí" / "No" |
| `matricula_al_dia` | `str` | Sí | "Sí" / "No" |
| `deudor` | `str` | Sí | "Sí" / "No" |
| `desplazado` | `str` | Sí | "Sí" / "No" |
| `tipo_vivienda` | `str` | Sí | "Propia" / "Alquilada" / "Familiar" |
| `ratio_aprobacion_sem1` | `float` | Sí | 0.0 - 1.0 |
| `ratio_aprobacion_sem2` | `float` | Sí | 0.0 - 1.0 |

**Example Request**
```json
{
  "edad": 20,
  "sexo": "M",
  "promedio_general": 12.5,
  "materias_repetidas": "No",
  "horas_tutoria": 2,
  "trabaja": "No",
  "ingreso_mensual": 800,
  "apoyo_familiar": "Alto",
  "responsabilidades_familiares": "Bajo",
  "becado": "Sí",
  "matricula_al_dia": "Sí",
  "deudor": "No",
  "desplazado": "No",
  "tipo_vivienda": "Propia",
  "ratio_aprobacion_sem1": 0.75,
  "ratio_aprobacion_sem2": 0.80
}
```

**Response** `200 OK` — `PredictionResponse`
```json
{
  "riesgo": 1,
  "probabilidad_riesgo": 0.7556,
  "nivel_riesgo": "Alto",
  "timestamp": "2026-05-28T19:31:48.444940Z"
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `riesgo` | `int` | 1 = Desertor, 0 = Continúa |
| `probabilidad_riesgo` | `float` | Probabilidad de deserción (0.0 - 1.0) |
| `nivel_riesgo` | `str` | "Bajo" (< 0.3) / "Medio" (< 0.6) / "Alto" (>= 0.6) |
| `timestamp` | `datetime` | Fecha/hora de la predicción (UTC) |

---

### 4. Predict Batch

```
POST /api/v1/predict/batch
Content-Type: application/json
```

**Request Body** — `BatchPredictionRequest`
```json
{
  "students": [
    { ...StudentFeatures },
    { ...StudentFeatures }
  ]
}
```

**Response** `200 OK` — `BatchPredictionResponse`
```json
{
  "predictions": [
    {
      "riesgo": 1,
      "probabilidad_riesgo": 0.7556,
      "nivel_riesgo": "Alto",
      "timestamp": "2026-05-28T19:31:48.515745Z"
    },
    {
      "riesgo": 1,
      "probabilidad_riesgo": 0.9389,
      "nivel_riesgo": "Alto",
      "timestamp": "2026-05-28T19:31:48.515775Z"
    }
  ],
  "total": 2
}
```

---

## Error Codes

| Código | Causa | Solución |
|---|---|---|
| `422` | Campos inválidos o faltantes | Revisar tipo/datos según tabla de arriba |
| `503` | Modelo no cargado | Ejecutar `python main.py --train` primero |

---

## Swagger UI

Documentación interactiva disponible en: `http://localhost:8000/docs`
