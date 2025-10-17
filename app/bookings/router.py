from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from datetime import date

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)

@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = jsonable_encoder(booking)
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict
