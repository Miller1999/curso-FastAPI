from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"
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
@app.get("/",tags=["Home"])
def message():
  return HTMLResponse("<h1>Hello world</h1>")
# Asi funciona get
@app.get("/movies",tags=["Movies"])
def get_movies():
  return movies
# Los parametros de ruta se colocan en la ruta
@app.get("/movies/{id}",tags=["Movies"])
def get_movie_by_id(id:int):
  for item in movies:
    if item["id"] == id:
      return item
  return []

@app.get("/movies/",tags=["Movies"])
# las query se colocan como parametros de las funciones
def get_movies_by_category(category:str):
  filtered = [movie for movie in movies if movie["category"] == category]
  return filtered

@app.post("/movies",tags=["Movies"])
def create_movies(id:int = Body(),title:str= Body(),overview:str= Body(),year:int= Body(),rating:float= Body(),category:str= Body()):
  movies.append({
    "id":id,
    "title":title,
    "overview":overview,
    "year":year,
    "rating":rating,
    "category":category
  })
  return movies