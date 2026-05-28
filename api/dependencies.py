from fastapi import Request, HTTPException, status


def get_model(request: Request) -> tuple:
    if not getattr(request.app.state, "model_loaded", False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo no cargado. Ejecuta entrenamiento primero.",
        )
    return request.app.state.model, request.app.state.threshold
