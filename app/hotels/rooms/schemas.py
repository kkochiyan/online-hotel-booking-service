from pydantic import BaseModel
from typing import Union

class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: Union[dict, list]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int