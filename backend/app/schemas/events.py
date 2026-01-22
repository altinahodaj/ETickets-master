from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Photo model
class PhotoModel(BaseModel):
    id: int
    file_path: str    # we will map this from EventPhoto.file_path

    model_config = {
        "from_attributes": True  # this replaces orm_mode in Pydantic v2
    }

# Response model for Event
class EventResponseModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    date: datetime
    is_paid: bool
    price: int
    attendees_number: int
    photos: List[PhotoModel] = []

    model_config = {
        "from_attributes": True
    }

# Request model for creating/updating Event
class EventCreateModel(BaseModel):
    name: str
    description: Optional[str] = None
    date: datetime
    is_paid: Optional[bool] = False
    price: Optional[int] = 0
    attendees_number: Optional[int] = 0
