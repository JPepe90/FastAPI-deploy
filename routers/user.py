from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.users import User

login_router = APIRouter()

@login_router.post('/login', tags=['auth'])
def login(user: User):
  token: str = create_token(user)
  return JSONResponse(status_code=200, content=token)