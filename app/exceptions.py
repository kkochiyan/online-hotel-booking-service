from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Пользователь уже существует'
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверная почта или пароль'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен истек'
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Токен отсутствует'
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный формат токена'
)

UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Не соталось свободных номеров'
)

NoRoomsInThisHotelException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Нет номеров в отеле'
)

NoHotelException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Нет такого отеля'
)

NoHotelsWithLeftRoomsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Нет отелей с свободными номерами'
)