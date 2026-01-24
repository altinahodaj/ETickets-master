from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List

class MovieTimeBase(BaseModel):
    hall_id: int = Field(..., alias="hallId")
    start_time: datetime = Field(..., alias="startTime")
    end_time: datetime = Field(..., alias="endTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HallSimpleResponse(BaseModel):
    id: int
    name: str
    hall_number: Optional[int] = Field(None, alias="hallNumber")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class MovieTimeCreate(MovieTimeBase):
    pass

class MovieTimeResponse(MovieTimeBase):
    id: int
    cinema_id: int = Field(..., alias="cinemaId")
    movie_id: int = Field(..., alias="movieId")
    deleted: bool
    hall: Optional[HallSimpleResponse] = None

class MovieTimeListResponse(BaseModel):
    result: List[MovieTimeResponse]
    errors: List[str] = []
    messages: List[str] = []
