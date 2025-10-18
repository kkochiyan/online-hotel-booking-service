from fastapi import Request, Depends
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timezone

from app.users.dao import UsersDAO
from app.config import settings
from app.exceptions import (TokenExpiredException, TokenAbsentException,
                            IncorrectTokenFormatException, UserIsNotPresentException)


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        decode_jwt = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = decode_jwt.get('sub')
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user