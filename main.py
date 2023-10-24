from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()

# Ajustes de la documentacion automatica de Swagger
app.title = 'Nueva aplicacion con FastAPI'
app.version = '0.0.1'

# Modelo de datos
class JWTBearer(HTTPBearer):
  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    data = validate_token(auth.credentials)

    if data['email'] != 'admin@admin':
      raise HTTPException(status_code=403, detail='Credenciales incorrectas')
    
    if not 'email' in data:
      raise HTTPException(status_code=401, detail='Token malformado')
    else:
      usuario = list(filter(lambda x: x['email'] == data['email'], users))
      if len(usuario) == 0:
        raise HTTPException(status_code=404, detail='Usuario inexistente')
      else:
        if data['password'] != usuario[0]['password']:
          raise HTTPException(status_code=403, detail='Credenciales incorrectas')


class User(BaseModel):
  email: str
  password: str

class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length = 3, max_length = 25)
  year: Optional[int] = Field(le = 2022), None
  rating: Optional[float] = Field(ge = 1, le = 10), None
  category: Optional[str] = Field(max_length = 25), None

  class Config:
    json_schema_extra = {
      "example": {
        'id': 1,
        'title': 'La sirenita',
        'year': 1987,
        'rating': 7.7,
        'category': 'Fantasia'
      }
    }

# datos hardcodeados para las pruebas de la API
movies = [
  {
    'id': 1,
    'title': 'Avatar',
    'year': 2012,
    'rating': 7.8,
    'category': 'Aventura'
  },
    {
    'id': 2,
    'title': 'El Origen',
    'year': 2014,
    'rating': 8.3,
    'category': 'Accion'
  },
  {
    "id": 3,
    "title": "Mi pobre Angelito",
    "year": 1986,
    "rating": 6.8,
    "category": "Comedia"
  }
]

users = [
  {
    'email': 'roberto@hml.com',
    'password': 'lalala'
  },
  {
    'email': 'laura@uol.com',
    'password': 'laura'
  },
  {
    'email': 'admin@admin',
    'password': 'admin'
  }
]


@app.get('/', tags=['home']) # con los tags tambien puedo modificar la documentacion
def message():
  return HTMLResponse('<h1>Inicio a la API con FastAPI</h1>')


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
  return JSONResponse(status_code=200, content=movies)


# Parametros de ruta
@app.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie_by_id(id: int = Path(get = 1, le = 10000)) -> Movie: # Validacion del parametro de ruta utilizando la libreria Path
  movie = list(filter(lambda x: x['id'] == id, movies))
  if len(movie) == 0:
    return JSONResponse(status_code=404, content={})
  else:
    return JSONResponse(status_code=200, content=movie[0])


# Parametros query --> agregar / al final para que no sobrescriba el metodo anterior
@app.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies_by_category(category: str = Query(min_length = 5)) -> List[Movie]: # Validacion del parametro de query
  return JSONResponse(status_code=200, content=list(filter(lambda x: x['category'] == category, movies)))


@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
  new_movie = {
    'id': movie.id,
    'title': movie.title,
    'year': movie.year,
    'rating': movie.rating,
    'category': movie.category
  }
  movies.append(new_movie)

  res = {
    'message': 'Pelicula creada',
    'data': new_movie
  }

  return JSONResponse(status_code=201, content=res)


@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, params: Movie) -> dict:
  indice = search_index(id)

  if indice == None:
    return JSONResponse(status_code=404, content={'message': 'No se encontro la pelicula solicitada'})
  else:
    for key, value in params.__dict__.items():
      movies[indice][key] = value

    res = {
      'message': 'Se actualizaron los datos de la pelicula con id ' + str(id),
      'data': movies[indice]
    }
    return JSONResponse(status_code=200, content=res)
  

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
  indice = search_index(id)

  res = {}
  if indice == None:
    res = {
      'message': 'No se encontro la pelicula solicitada'
    }
  else:
    movies.pop(indice)
    res = {
      'message': 'Se elemino la pelicula con id: ' + str(id)
    }
  return JSONResponse(status_code=200, content=res)

@app.post('/login', tags=['auth'])
def login(user: User):
  token: str = create_token(user)
  return JSONResponse(status_code=200, content=token)


######################################################################
# Funciones auxiliares
def search_index(id):
  indice = None
  for m in movies:
    if m['id'] == id:
      indice = movies.index(m)
      break
  return indice