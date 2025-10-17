from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings

from datetime import date
from sqlalchemy import select, func, case, or_, and_

class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_for_hotels(
            cls,
            location: str,
            date_from: date,
            date_to: date,
    ):
        async with async_session_maker() as session:
            booked_rooms = select(
                Rooms.id,
                Rooms.hotel_id,
                func.count(
                    case(
                        (
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from
                                )
                            ),
                            Bookings.id
                        ),
                        else_=None
                    )
                ).label("booked_rooms_quantity")
            ).outerjoin(Bookings, Bookings.room_id == Rooms.id).group_by(Rooms.id).cte("booked_rooms")

            get_hotel_with_rooms_left = select(
                Hotels.id,
                Hotels.name,
                Hotels.location,
                Hotels.services,
                Hotels.rooms_quantity,
                Hotels.image_id,
                (Hotels.rooms_quantity - func.coalesce(func.sum(booked_rooms.c.booked_rooms_quantity), 0)).label("rooms_left")
            ).outerjoin(
                booked_rooms, booked_rooms.c.hotel_id == Hotels.id
            ).where(Hotels.location.ilike(f"%{location}%")).group_by(Hotels.id).having(
                (Hotels.rooms_quantity - func.coalesce(func.sum(booked_rooms.c.booked_rooms_quantity), 0)) > 0
            )

            hotels_with_rooms_left = await session.execute(get_hotel_with_rooms_left)
            hotels_with_rooms_left = hotels_with_rooms_left.all()

            if len(hotels_with_rooms_left) > 0:
                return hotels_with_rooms_left
            else:
                return None