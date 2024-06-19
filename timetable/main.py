from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings

from api.users import router as api_router
from api.profile import router as profile_router
from api.trener import router as trener_router
from authentication.auth import router as auth_router
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan,)
main_app.include_router(api_router,)
main_app.include_router(auth_router,)
main_app.include_router(profile_router,)
main_app.include_router(trener_router,)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )