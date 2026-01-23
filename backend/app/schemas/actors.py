from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class ActorBase(BaseModel):
    firstName: str
    lastName: str
    imgPath: Optional[str] = None
    nationality: Optional[str] = None
    genre: Optional[str] = None
    birth: Optional[date] = None

class ActorCreate(ActorBase):
    pass

class ActorResponse(ActorBase):
    id: int
    deleted: bool
    photos: List[str] = []

    model_config = {
        "from_attributes": True
    }
