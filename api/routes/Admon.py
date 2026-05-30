from http.client import HTTPException
from fastapi import APIRouter, status

from src.schemas import Admon

router = APIRouter(tags=["Admon"])

admin=[]

@router.get("/admins", response_model=list[Admon])
async def get_all_admins():
    return admin    

@router.post("/admin", response_model=Admon)
async def create_admin(admin_data: Admon):
    admin.append(admin_data)
    return admin_data