from fastapi import Path, Query,Depends,APIRouter
from fastapi.responses import  JSONResponse
from typing import List
from config.database import session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get("/movies",tags=["Movies"],response_model=List[Movie],dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = session()
  result = MovieService(db).get_movies()
  return JSONResponse(content=jsonable_encoder(result))
# Los parametros de ruta se colocan en la ruta, con Path nos permite hacer validaciones como en Field pero en los parametros de ruta
@movie_router.get("/movies/{id}",tags=["Movies"])
def get_movie_by_id(id:int = Path(ge=1,le=2000)):
  db = session()
  result = MovieService(db).get_movie_by_id(id)
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.get("/movies/",tags=["Movies"])
# las query se colocan como parametros de las funciones, de igual manera con Query para los parametros Query
def get_movies_by_category(category:str = Query(min_length=5,max_length=15)):
  db = session()
  result = MovieService(db).get_movie_by_category(category)
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"}) 
  return JSONResponse(status_code=200,content=jsonable_encoder(result))

@movie_router.post("/movies",tags=["Movies"])
def create_movies(movie: Movie):
  db = session()
  MovieService(db).create_movie(movie)
  return JSONResponse(content={"message":"Se ha registrado la pelicula"})

@movie_router.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie:Movie):
  db= session()
  result = MovieService(db).get_movie_by_id(id)
  if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
  MovieService(db).update_movie(id,movie)
  db.commit()
  return JSONResponse(content={"message":"Se ha actualizado la pelicula"})

@movie_router.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
    db= session()
    result = MovieService(db).get_movie_by_id(id)
    if not result:
      return JSONResponse(status_code=404,content={"message": "No encontrado"})
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message":"Se ha eliminado la pelicula"})