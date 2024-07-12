from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine,Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi primera api con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


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



