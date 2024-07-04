from fastapi import FastAPI
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

@app.get("/",tags=["Home"])
def message():
  return HTMLResponse("<h1>Hello world</h1>")
# Asi funciona get
@app.get("/movies",tags=["Movies"])
def get_movies():
  return movies

@app.get("/movies/{id}",tags=["Movies"])
def get_movie_by_id(id:int):
  for item in movies:
    if item["id"] == id:
      return item
  return []