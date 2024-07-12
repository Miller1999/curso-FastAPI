from fastapi import FastAPI, Body, Path, Query, Request, HTTPException,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token,validate_token
from fastapi.security import HTTPBearer
from config.database import session,engine,Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

# Clase para poder autenticar el acceso 
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403,detail="Credenciales invalidas")
class User(BaseModel):
    email:str
    password:str

# Se crea esto para evitar pasar todo por parametro, esto es similar a las interfaces de typescript
#  Se extiende de BaseModel, Field se usa para validaciones
class Movie(BaseModel):
    id: Optional[int] = None # De esta manera se puede hacer un modo opcional para este parametro
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=150)
    year: int = Field(le=2022)
    rating: float = Field(le=10.0,ge=0)
    category: str = Field(min_length=5,max_length=15)

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
# Informacion de ejemplo
movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},{
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]
# tags funciona para la documentacion, a esta se accede con /docs
# Con la clase JSONResponse retornamos una respuesta JSON, lo caul nos sirve para la API, pero lo que vamos a devolver va dentro de content
@app.get("/",tags=["Home"])
def message():
  return HTMLResponse("<h1>Hello world</h1>")
# Asi funciona get
# Con response model especificamos que output vamos a tener de la misma manera en las fuciones con ->
# usando la funcion Depends validamos que el usuario tenga permisos para acceder a este endpoint
@app.get("/movies",tags=["Movies"],response_model=List[Movie],dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = session()
  result = db.query(MovieModel).all()
  return JSONResponse(content=jsonable_encoder(result))
# Los parametros de ruta se colocan en la ruta, con Path nos permite hacer validaciones como en Field pero en los parametros de ruta
@app.get("/movies/{id}",tags=["Movies"])
def get_movie_by_id(id:int = Path(ge=1,le=2000)):
  db = session()
  result = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.post("/login",tags=["Auth"])
def login(user:User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.model_dump())
    return JSONResponse(status_code=200,content=token)

@app.get("/movies/",tags=["Movies"])
# las query se colocan como parametros de las funciones, de igual manera con Query para los parametros Query
def get_movies_by_category(category:str = Query(min_length=5,max_length=15)):
  db = session()
  result = db.query(MovieModel).filter(MovieModel.category == category).all()
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"}) 
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

@app.post("/movies",tags=["Movies"])
def create_movies(movie: Movie):
  db = session()
  new_movie = MovieModel(**movie.model_dump())
  db.add(new_movie)
  db.commit()
  return JSONResponse(content={"message":"Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie:Movie):
  db= session()
  result = db.query(MovieModel).filter(MovieModel.id == id).first()
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
  result.title = movie.title
  result.overview = movie.overview
  result.year = movie.year
  result.rating = movie.rating
  result.category = movie.category
  db.commit()
  return JSONResponse(content={"message":"Se ha actualizado la pelicula"})

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    db= session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message":"Se ha eliminado la pelicula"})