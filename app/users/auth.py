from passlib.context import CryptContext
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.users.dao import UsersDAO
from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_paswword: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_paswword, hashed_password)

async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encode_jwt
