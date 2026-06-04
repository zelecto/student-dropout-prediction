from http.client import HTTPException
from fastapi import APIRouter, status

from src.schemas import StudentFeatures, LoginRequest

router = APIRouter(tags=["StudentFeatures"])

user: list[StudentFeatures] = []


@router.post("/student", response_model=StudentFeatures)
async def create_student_features(student: StudentFeatures):
    user.append(student)
    return student


@router.get("/students/edad", response_model=list[StudentFeatures])
async def get_all_students(edad_min: int | None = None, edad_max: int | None = None):
    """
    Obtiene la lista de estudiantes con filtro opcional de edad.
    
    Query Parameters:
    - edad_min: Edad mínima (inclusive)
    - edad_max: Edad máxima (inclusive)
    
    Ejemplo: /students?edad_min=18&edad_max=25
    """
    estudiantes_filtrados = user
    
    if edad_min is not None:
        estudiantes_filtrados = [s for s in estudiantes_filtrados if s.edad >= edad_min]
    
    if edad_max is not None:
        estudiantes_filtrados = [s for s in estudiantes_filtrados if s.edad <= edad_max]
    
    return estudiantes_filtrados


@router.get("/students/sexo", response_model=list[StudentFeatures])
async def get_students_by_sexo(sexo: str):
    """
    Obtiene la lista de estudiantes filtrados por sexo.
    
    Query Parameters:
    - sexo: Sexo a filtrar (M/F)
    
    Ejemplo: /students/sexo?sexo=M
    """
    return [s for s in user if s.sexo.upper() == sexo.upper()]


@router.get("/students/beca", response_model=list[StudentFeatures])
async def get_students_by_beca(becado: str):
    """
    Obtiene la lista de estudiantes filtrados por estado de beca.
    
    Query Parameters:
    - becado: Estado de beca (Sí/No)
    
    Ejemplo: /students/beca?becado=Sí
    """
    return [s for s in user if s.becado.lower() == becado.lower()]


@router.get("/students/promedio", response_model=list[StudentFeatures])
async def get_students_by_promedio(promedio_min: float | None = None, promedio_max: float | None = None):
    """
    Obtiene la lista de estudiantes filtrados por rango de promedio general.
    
    Query Parameters:
    - promedio_min: Promedio mínimo (inclusive)
    - promedio_max: Promedio máximo (inclusive)
    
    Ejemplo: /students/promedio?promedio_min=3.0&promedio_max=4.5
    """
    estudiantes_filtrados = user
    
    if promedio_min is not None:
        estudiantes_filtrados = [s for s in estudiantes_filtrados if s.promedio_general >= promedio_min]
    
    if promedio_max is not None:
        estudiantes_filtrados = [s for s in estudiantes_filtrados if s.promedio_general <= promedio_max]
    
    return estudiantes_filtrados


@router.get("/students/trabaja", response_model=list[StudentFeatures])
async def get_students_by_trabaja(trabaja: str):
    """
    Obtiene la lista de estudiantes según su situación laboral.
    
    Query Parameters:
    - trabaja: Estado laboral (Sí/No)
    
    Ejemplo: /students/trabaja?trabaja=Sí
    """
    return [s for s in user if s.trabaja.lower() == trabaja.lower()]


@router.get("/students/apoyo", response_model=list[StudentFeatures])
async def get_students_by_apoyo(apoyo_familiar: str):
    """
    Obtiene la lista de estudiantes filtrados por apoyo familiar.
    
    Query Parameters:
    - apoyo_familiar: Nivel de apoyo familiar
    
    Ejemplo: /students/apoyo?apoyo_familiar=Alto
    """
    return [s for s in user if s.apoyo_familiar.lower() == apoyo_familiar.lower()]

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

