from http.client import HTTPException
from fastapi import APIRouter, Request, status

from src.schemas import StudentFeatures, ModelInfo

router = APIRouter(tags=["StudentFeatures"])

user=[]


@router.post("/student", response_model=StudentFeatures)
async def create_student_features(student: StudentFeatures):
    user.append(student)
    return student

@router.get("/students", response_model=list[StudentFeatures])
async def get_all_students():
    return user

@router.post("/student/login")
async def login_student(student: StudentFeatures):
    for s in user:
        if (s.correo != student.correo or s.contraseña != student.contraseña):
            return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
            ) 
        else: return {"message": "Login exitoso"}