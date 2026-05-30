from datetime import datetime, UTC

from fastapi import APIRouter

from src.database import get_indicadores_dashboard
from src.schemas import DashboardResponse

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard():
    indicadores = get_indicadores_dashboard()
    indicadores["actualizado_el"] = datetime.now(UTC)
    return indicadores