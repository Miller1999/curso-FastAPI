from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"

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
@app.get("/movies",tags=["Movies"],response_model=List[Movie])
def get_movies() -> List[Movie]:
  return JSONResponse(content=movies)
# Los parametros de ruta se colocan en la ruta, con Path nos permite hacer validaciones como en Field pero en los parametros de ruta
@app.get("/movies/{id}",tags=["Movies"])
def get_movie_by_id(id:int = Path(ge=1,le=2000)):
  for item in movies:
    if item["id"] == id:
      return JSONResponse(content=item)
  return JSONResponse(status_code=404,content=[])

@app.post("/login",tags=["Auth"])
def login(user:User):
    return user

@app.get("/movies/",tags=["Movies"])
# las query se colocan como parametros de las funciones, de igual manera con Query para los parametros Query
def get_movies_by_category(category:str = Query(min_length=5,max_length=15)):
  filtered = [movie for movie in movies if movie["category"] == category]
  return JSONResponse(content=filtered)

@app.post("/movies",tags=["Movies"])
def create_movies(movie: Movie):
  movies.append(movie)
  return JSONResponse(content={"message":"Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie:Movie):
	for item in movies:
		if item['id'] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return JSONResponse(content={"message":"Se ha actualizado la pelicula"})
        
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(content={"message":"Se ha eliminado la pelicula"})