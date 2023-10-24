from jwt import encode, decode
import config

def create_token(data: dict) -> str:
  token: str = encode(payload=dict(data), key=config.my_secret_jwt, algorithm='HS256')
  return token

def validate_token(token:str) -> dict:
  data: dict = decode(token, key=config.my_secret_jwt, algorithms=['HS256'])
  return data