from fastapi import APIRouter, HTTPException, Query

from src.database import get_estudiantes_con_predicciones, get_estudiante_detallado, init_db
from src.schemas import HistorialEstudianteResponse, PaginatedEstudiantesResponse

router = APIRouter(prefix="/api/v1", tags=["Historial"])

PAGE_SIZE = 20


@router.get("/estudiantes", response_model=PaginatedEstudiantesResponse)
async def listar_estudiantes(
    pagina: int = Query(1, ge=1, description="Número de página"),
    por_pagina: int = Query(PAGE_SIZE, ge=1, le=100, description="Registros por página"),
):
    init_db()
    estudiantes, total = get_estudiantes_con_predicciones(pagina, por_pagina)
    total_paginas = (total + por_pagina - 1) // por_pagina

    return PaginatedEstudiantesResponse(
        data=estudiantes,
        total=total,
        pagina=pagina,
        por_pagina=por_pagina,
        total_paginas=total_paginas,
    )


@router.get("/estudiantes/{estudiante_id}", response_model=HistorialEstudianteResponse)
async def obtener_estudiante(estudiante_id: int):
    init_db()
    estudiante = get_estudiante_detallado(estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante