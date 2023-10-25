from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from jwt_manager import create_token, validate_token

class JWTBearer(HTTPBearer):
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validate_token(auth.credentials)

    if data['email'] != 'admin@admin':
      raise HTTPException(status_code=403, detail='Credenciales incorrectas')
    
    if not 'email' in data:
      raise HTTPException(status_code=401, detail='Token malformado')
    else:
      usuario = list(filter(lambda x: x['email'] == data['email'], users))
      if len(usuario) == 0:
        raise HTTPException(status_code=404, detail='Usuario inexistente')
      else:
        if data['password'] != usuario[0]['password']:
          raise HTTPException(status_code=403, detail='Credenciales incorrectas')