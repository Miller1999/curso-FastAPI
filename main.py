from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"

# Se crea esto para evitar pasar todo por parametro, esto es similar a las interfaces de typescript
class Movie(BaseModel):
    id: Optional[int] = None # De esta manera se puede hacer un modo opcional para este parametro
    title: str
    overview: str
    year: int
    rating: float
    category: str
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
def create_movies(movie: Movie):
  movies.append(movie)
  return movies

@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie:Movie):
	for item in movies:
		if item['id'] == id:
			item['title'] = movie.title
			item['overview'] = movie.overview
			item['year'] = movie.year
			item['rating'] = movie.rating
			item['category'] = movie.category
			return movies 
        
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return movies