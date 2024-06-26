from typing import Dict

from fastapi import APIRouter
from fastapi import Depends

from src.auth import create_jwt_token
from src.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/token")
async def generate_token():
    # Para simplificar, vamos gerar um token sem qualquer autenticação real.
    # Em um cenário real, você deve verificar as credenciais do usuário antes de gerar um token.
    user_data = {"user_id": "123", "username": "user"}
    token = create_jwt_token(user_data)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/user")
async def get_production(current_user: Dict = Depends(get_current_user)):
    return {"message": f"Hello {current_user['username']}"}
