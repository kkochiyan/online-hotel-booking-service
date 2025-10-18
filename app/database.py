from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import NullPool

from app.config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_ASYNC_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.ASYNC_DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(
    DATABASE_URL,
    **DATABASE_PARAMS
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass