from fastapi import APIRouter
from fastapi_cache.decorator import cache
from datetime import date

from app.hotels.schemas import SHotel, SHotels
from app.hotels.dao import HotelDAO
from app.exceptions import NoHotelException, NoHotelsWithLeftRoomsException

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)

@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(location: str, date_from: date, date_to: date):
    hotels = await HotelDAO.search_for_hotels(location, date_from, date_to)

    if not hotels:
        raise NoHotelsWithLeftRoomsException

    hotels_models = [SHotels.model_validate(dict(row._mapping)) for row in hotels]

    return hotels_models


@router.get('/id/{hotel_id}')
async def get_hotel(hotel_id: int) -> list[SHotel]:
    hotel = await HotelDAO.find_all(id=hotel_id)
    if not hotel:
        raise NoHotelException
    return hotel