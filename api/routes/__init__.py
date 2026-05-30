from api.routes.health import router as health_router
from api.routes.prediction import router as prediction_router
from api.routes.dashboard import router as dashboard_router

__all__ = ["health_router", "prediction_router", "dashboard_router"]