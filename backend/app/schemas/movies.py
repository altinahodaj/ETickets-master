from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

class PhotoResponse(BaseModel):
    id: str
    cinema_id: Optional[int] = Field(None, alias="cinemaId")
    movie_id: Optional[int] = Field(None, alias="movieId")
    photo_type: str = Field(..., alias="photoType")
    name: str
    img_path: str = Field(..., alias="imgPath")
    img_client_path: str = Field(..., alias="imgClientPath")

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None
    length_minutes: Optional[int] = Field(0, alias="lengthMinutes")
    release_year: Optional[int] = Field(None, alias="releaseYear")
    director: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )

class MovieCreate(MovieBase):
    pass

class MovieResponse(MovieBase):
    id: int
    cinema_id: int = Field(..., alias="cinemaId")
    avg_rating: float = Field(0.0, alias="avgRating")
    total_reviews: int = Field(0, alias="totalReviews")
    deleted: bool
    photos: List[PhotoResponse] = []
    actors: List[dict] = [] # Placeholder for now to avoid crashes

class MovieListResponse(BaseModel):
    result: List[MovieResponse]
    errors: List[str] = []
    messages: List[str] = []

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )
