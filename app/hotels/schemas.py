from pydantic import BaseModel
from typing import Union

class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: Union[dict, list]
    rooms_quantity: int
    image_id: int
    rooms_left: int


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Union[dict, list]
    rooms_quantity: int
    image_id: int