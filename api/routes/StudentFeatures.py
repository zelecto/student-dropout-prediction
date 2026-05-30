from http.client import HTTPException
from fastapi import APIRouter, status

from src.schemas import StudentFeatures, LoginRequest

router = APIRouter(tags=["StudentFeatures"])

user: list[StudentFeatures] = []


@router.post("/student", response_model=StudentFeatures)
async def create_student_features(student: StudentFeatures):
    user.append(student)
    return student


@router.get("/students", response_model=list[StudentFeatures])
async def get_all_students():
    return user


@router.post("/student/login")
async def login_student(credentials: LoginRequest):
    for s in user:
        if s.correo == credentials.correo and s.contraseña == credentials.contraseña:
            return {"message": "Login exitoso"}
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas"
    )