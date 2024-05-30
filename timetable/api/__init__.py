from fastapi import APIRouter

from timetable.core.config import settings

router = APIRouter(
    prefix=settings.api.prefix,
)