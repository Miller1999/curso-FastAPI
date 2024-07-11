# Se instala PyJWT, para generar tokens para el cifrado
# Se importa
from jwt import encode

def create_token(data:dict):
  token:str = encode(payload=data,key="my_secret_key",algorithm="HS256")