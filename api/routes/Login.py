from fastapi import APIRouter, HTTPException, status

from api.routes.Admon import admin as admin_list
from src.schemas import LoginRequest

router = APIRouter(tags=["Login"])


@router.post("/login")
async def login_admin(credentials: LoginRequest):
    for adm in admin_list:
        if adm.correo == credentials.correo and adm.contraseña == credentials.contraseña:
            return {
                "message": "Login exitoso",
                "admin": {
                    "correo": adm.correo,
                    "Nombre": adm.Nombre,
                    "Apellido": adm.Apellido,
                },
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas",
    )

