from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

class SeatResponse(BaseModel):
    id: int
    cinema_id: int = Field(..., alias="cinemaId")
    hall_id: int = Field(..., alias="hallId")
    row_id: int = Field(..., alias="rowId")
    seat_name: str = Field(..., alias="seatName")
    is_vip_seat: bool = Field(False, alias="isVipSeat")
    is_couple_seat: bool = Field(False, alias="isSeatForCouple")
    deleted: bool

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class RowResponse(BaseModel):
    id: int
    cinema_id: int = Field(..., alias="cinemaId")
    hall_id: int = Field(..., alias="hallId")
    row_name: str = Field(..., alias="rowName")
    number_of_seats: int = Field(..., alias="numberOfSeats")
    is_vip_row: bool = Field(False, alias="isVipRow")
    deleted: bool
    seats: List[SeatResponse] = []

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HallResponse(BaseModel):
    id: int
    cinema_id: int = Field(..., alias="cinemaId")
    name: str
    hall_number: Optional[int] = Field(None, alias="hallNumber")
    number_of_rows: Optional[int] = Field(None, alias="numberOfRows")
    has_3d: bool = Field(False, alias="has3D")
    deleted: bool
    rows: List[RowResponse] = []

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
