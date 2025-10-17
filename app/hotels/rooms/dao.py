from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings

from datetime import date
from sqlalchemy import select, func, case, and_, or_

class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def search_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            booked_rooms = select(
                Rooms.id,
                Rooms.hotel_id,
                func.coalesce(
                    func.count(
                        case(
                            (
                                or_(
                                    and_(
                                        Bookings.date_from >= date_from,
                                        Bookings.date_from < date_to
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
                    ), 0
                ).label("booked_rooms_quantity")
            ).join(Bookings, Bookings.room_id == Rooms.id, isouter=True
                   ).where(Rooms.hotel_id == hotel_id
                           ).group_by(Rooms.id).cte("booked_rooms")

            # Итоговый запрос
            get_rooms_by_time = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * func.extract('epoch', (date_to - date_from)) / 86400).label("total_cost"),
                (Rooms.quantity - func.coalesce(func.sum(booked_rooms.c.booked_rooms_quantity), 0)).label("rooms_left")
            ).join(booked_rooms, booked_rooms.c.id == Rooms.id, isouter=True
                   ).where(
                Rooms.hotel_id == hotel_id,
            ).group_by(Rooms.id)

            rooms_by_time = await session.execute(get_rooms_by_time)
            rooms_by_time = rooms_by_time.fetchall()


            if len(rooms_by_time) > 0:
                return rooms_by_time
            else:
                return None