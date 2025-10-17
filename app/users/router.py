from fastapi import APIRouter, Response, Depends

from app.users.shemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_hashed_password, authenticate_user, create_access_token
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException


router = APIRouter(
    prefix='/auth',
    tags=['Auth & Пользователи']
)

@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistException
    hashed_password = get_hashed_password(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(user_data: SUserAuth, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user