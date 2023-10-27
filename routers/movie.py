from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder
from config.database import Session
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from schemas.movies import Movie

# Service Import
from services.movie import MovieService

movie_router = APIRouter()

@movie_router.get('/', tags=['home']) # con los tags tambien puedo modificar la documentacion
def message():
  return HTMLResponse('<h1>Inicio a la API con FastAPI</h1>')


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  db = Session()
  result = MovieService(db).get_movies()
  return JSONResponse(status_code=200, content=jsonable_encoder(result))


# Parametros de ruta
@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie_by_id(id: int = Path(get = 1, le = 10000)) -> Movie: # Validacion del parametro de ruta utilizando la libreria Path
  db = Session()
  movie = MovieService(db).get_movie_by_id(id)

  if not movie:
    return JSONResponse(status_code=404, content={'message': 'pelicula no encontrada'})
  else:
    return JSONResponse(status_code=200, content=jsonable_encoder(movie))


# Parametros query --> agregar / al final para que no sobrescriba el metodo anterior
@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length = 5)) -> List[Movie]: # Validacion del parametro de query
  db = Session()
  result = MovieService(db).get_movie_by_category(category)

  return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
  db = Session()
  result = MovieService(db).create_movie(movie)

  if not result:
    return JSONResponse(status_code=500, content={'message': 'No se pudo registrar la pelicula'})
  return JSONResponse(status_code=201, content={'message': 'Pelicula creada'})



@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, params: Movie) -> dict:
  db = Session()
  result, status = MovieService(db).update_movie(id, params)

  if not result:
    if status == 404:
      return JSONResponse(status_code=404, content={'message': 'No se pudo encontrar la pelicula solicitada'})      
    return JSONResponse(status_code=500, content={'message': 'Hubo un problema al actualizar la pelicula solicitada'})

  return JSONResponse(status_code=200, content={'message': 'Se actualizaron los datos de la pelicula con id ' + str(id)})
  

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
  db = Session()
  result, status = MovieService(db).delete_movie(id)

  if not result:
    if status == 404:
      return JSONResponse(status_code=404, content={'message': 'no se encontró la pelicula indicada'})
    return JSONResponse(status_code=500, content={'message': 'Hubo un problema al eliminar la pelicula indicada'})
  
  return JSONResponse(status_code=200, content={'message': 'Se elemino la pelicula con id: ' + str(id)})
