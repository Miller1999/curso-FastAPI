from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
user_router = APIRouter()

# Clase para poder autenticar el acceso 
class User(BaseModel):
    email:str
    password:str

# Se crea esto para evitar pasar todo por parametro, esto es similar a las interfaces de typescript
#  Se extiende de BaseModel, Field se usa para validaciones


# Con este diccionario model_config se puede establecer el ejemplo de la informacion que debe llevar el body
    model_config = {
        "json_schema_extra": {
            "examples":[
                {
                "id":1,
                "title":"Mi pelicula",
                "overview":"Descripcion de la pelicula",
                "year":2022,
                "rating":9.8,
                "category":"Accion"}
            ]
        }
    }

@user_router.post("/login",tags=["Auth"])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.model_dump())
    return JSONResponse(status_code=200,content=token)