from pydantic import BaseModel

# Clase para poder autenticar el acceso 
class User(BaseModel):
    email:str
    password:str

# Se crea esto para evitar pasar todo por parametro, esto es similar a las interfaces de typescript
#  Se extiende de BaseModel, Field se usa para validaciones