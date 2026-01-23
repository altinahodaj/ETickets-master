from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import List, Optional

# Photo model
class PhotoModel(BaseModel):
    id: int
    file_path: str    # we will map this from EventPhoto.file_path
    imgClientPath: Optional[str] = None

    model_config = {
        "from_attributes": True  # this replaces orm_mode in Pydantic v2
    }

    @model_validator(mode="after")
    def set_img_client_path(self):
        from app.core.config import settings
        # file_path në DB mund të jetë "uploads/events/filename.jpg"
        if not self.file_path:
             self.imgClientPath = f"{settings.STATIC_BASE_URL}/assets/app_files/Movies/default-image.jpg"
             return self

        # Pastro slashes nese ka mbetur ndonje \ nga Windows
        fixed_path = self.file_path.replace("\\", "/")
        
        if not fixed_path.startswith("http"):
            # Sigurohu qe nuk ka double slashes nese fixed_path fillon me /
            path_suffix = fixed_path if not fixed_path.startswith("/") else fixed_path[1:]
            self.imgClientPath = f"{settings.STATIC_BASE_URL}/{path_suffix}"
        else:
            self.imgClientPath = fixed_path
        return self

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
