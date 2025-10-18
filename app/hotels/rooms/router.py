from datetime import date, datetime, timedelta

from fastapi import Query, APIRouter

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRoomInfo
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/hotels',
    tags=['Комнаты']
)

@router.get('/{hotel_id}/rooms')
@cache(expire=30)
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Наример, {(datetime.now() + timedelta(days=14)).date()}")
) -> list[SRoomInfo]:
    rooms = await RoomDAO.find_all(hotel_id, date_from, date_to)
    return rooms
