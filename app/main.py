import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.images.router import router as router_images
from app.importer.router import router as router_import
from app.pages.router import router as router_pages
from app.users.router import router_auth, router_users
from app.logger import logger

#Подключение кэша
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield

#Создание приложения FastAPI
app = FastAPI(
    title='Бронирование отелей',
    lifespan=lifespan
)

#Подлкючение sentry для мониторинга ошибок
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    send_default_pii=True,
)

# Подключение основных роутеров
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_auth)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_import)
app.include_router(router_images)


#Монтирование статических файлов
app.mount('/static', StaticFiles(directory='app/static'), 'static')


#Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

#Подключение админки
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)


#Подключение middleware
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
#     return response