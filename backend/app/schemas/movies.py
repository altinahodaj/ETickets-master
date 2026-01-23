from pydantic import BaseModel
from typing import List, Optional

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    length_minutes: Optional[int] = 0
    release_year: Optional[int] = None
    director: Optional[str] = None

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    cinema_id: int
    avg_rating: float = 0.0
    total_reviews: int = 0
    deleted: bool = False

    model_config = {
        "from_attributes": True
    }
