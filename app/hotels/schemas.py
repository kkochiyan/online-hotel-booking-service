from pydantic import BaseModel
from typing import Union


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Union[dict, list]
    rooms_quantity: int
    image_id: int

class SHotelInfo(SHotel):
    rooms_left: int