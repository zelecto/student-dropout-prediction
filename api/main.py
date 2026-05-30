from datetime import datetime, UTC
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import health_router, prediction_router
from api.routes.StudentFeatures import router as student_router
from src.predict import load_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        modelo, threshold = load_model()
        app.state.model = modelo
        app.state.threshold = threshold
        app.state.model_loaded_at = datetime.now(UTC)
        app.state.model_loaded = True
    except FileNotFoundError:
        app.state.model_loaded = False
        app.state.model = None
        app.state.threshold = 0.5
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Student Dropout Prediction API",
        description="API para predicción de deserción estudiantil con Random Forest",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(prediction_router)
    app.include_router(student_router)
    return app
