from contextlib import asynccontextmanager
from redis import asyncio as aioredis

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from core.config import settings
from core.models import db_helper
from api.users import router as api_router
from api.profile import router as profile_router
from api.trener import router as trener_router
from api.timetable import router as timetable_router
from api.login import router as login_router
from tasks.router import router as tasks_router
from authentication.auth import router as auth_router
from pages.router import router as pages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # startup
    print("BD connect")
    await startup_event_redis()
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)

# main_app.mount("/static", StaticFiles(directory="static"), name="static")

main_app.include_router(api_router)
main_app.include_router(auth_router, )
main_app.include_router(profile_router)
main_app.include_router(trener_router)
main_app.include_router(timetable_router)
main_app.include_router(pages_router)
main_app.include_router(login_router)
main_app.include_router(tasks_router)


async def startup_event_redis():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = [
    "http://localhost",
    "http://localhost:8000",
]

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    # allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    # allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
    #                "Authorization"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
