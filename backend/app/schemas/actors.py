from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PhotoOut(BaseModel):
    id: str
    imgClientPath: str


class ActorCreate(BaseModel):
    firstName: str
    lastName: str
    imgPath: Optional[str] = None
    nationality: Optional[str] = None
    genre: Optional[str] = None
    birth: Optional[datetime] = None


class ActorResponse(BaseModel):
    id: int
    firstName: str
    lastName: str
    imgPath: Optional[str] = None
    nationality: Optional[str] = None
    genre: Optional[str] = None
    birth: Optional[datetime] = None
    deleted: bool = False
    photos: List[PhotoOut] = Field(default_factory=list)
