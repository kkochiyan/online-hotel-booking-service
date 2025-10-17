from fastapi import APIRouter
from datetime import date

from app.hotels.rooms.dao import RoomDAO
from app.exceptions import NoRoomsInThisHotelException
from app.hotels.rooms.schemas import SRoom

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_time(hotel_id: int, date_from: date, date_to: date) -> list[SRoom]:
    rooms = await RoomDAO.search_rooms(hotel_id, date_from, date_to)
    if not rooms:
        raise NoRoomsInThisHotelException
    return rooms
