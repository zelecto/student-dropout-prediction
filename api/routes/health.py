from fastapi import APIRouter, Request

from src.schemas import HealthResponse, ModelInfo

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(request: Request):
    model_loaded = getattr(request.app.state, "model_loaded", False)
    model_info = None
    if model_loaded:
        model_info = ModelInfo(
            features=[],
            threshold=getattr(request.app.state, "threshold", 0.5),
            loaded_at=getattr(request.app.state, "model_loaded_at", None),
        )
    return HealthResponse(
        status="ok" if model_loaded else "degraded",
        model_loaded=model_loaded,
        model_info=model_info,
    )
