from pydantic import BaseModel, Field
from typing import Optional, List

class Movie(BaseModel):
  id: Optional[int] = None
  title: str = Field(min_length = 3, max_length = 25)
  year: Optional[int] = Field(le = 2022), None
  rating: Optional[float] = Field(ge = 1, le = 10), None
  category: Optional[str] = Field(max_length = 25), None

  class Config:
    json_schema_extra = {
      "example": {
        'title': 'La sirenita',
        'year': 1987,
        'rating': 7.7,
        'category': 'Fantasia'
      }
    }