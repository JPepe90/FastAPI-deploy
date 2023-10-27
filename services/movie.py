from models.movie import Movie as MovieModel
from schemas.movies import Movie

class MovieService():
  def __init__(self, db) -> None:
    self.db = db
  
  def get_movies(self):
    result = self.db.query(MovieModel).all()
    return result
  
  def get_movie_by_id(self, id) -> None:
    result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
    return result
  
  def get_movie_by_category(self, category) -> None:
    result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
    return result
  
  def create_movie(self, movie: Movie) -> True or False:
    try:
      new_movie = MovieModel(**movie.model_dump())
      self.db.add(new_movie)
      self.db.commit()
      return True
    except Exception as e:
      print({
        'error': str(e)
      })

      return False
  
  def update_movie(self, id: int, data: Movie) -> True or False:
    pelicula = self.db.query(MovieModel).filter(MovieModel.id == id).first()

    if not pelicula:
      return [False, 404]

    try:
      setattr(pelicula, 'id', id)
      for key, value in data.__dict__.items():
        if key != 'id':
          setattr(pelicula, key, value)
      self.db.commit()

      return [True, 200]
    except Exception as e:
      print({
        'error': str(e)
      })

      return [False, 500]
    
  def delete_movie(self, id):
    pelicula = self.db.query(MovieModel).filter(MovieModel.id == id).first()

    if not pelicula:
      return [False, 404]
    
    try:
      self.db.delete(pelicula)
      self.db.commit()

      return [True, 200]
    except Exception as e:
      print({
        'error': str(e)
      })
      
      return [False, 500]