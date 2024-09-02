from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from authentication.utils import http_bearer
from core.config import settings
from core.models import db_helper, Timetable
from core.schemas.timetable import TimetableRead, TimetableCreate
from core.schemas.user import UserRead
from crud import timetable as timetable_crud
from utils.dependencies import timetable_by_id
from utils.validate_token import get_current_token_payload

router = APIRouter(tags=["Tametable"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.post("timetable/create", response_model=TimetableRead)
async def create_timetable(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        timetable_create: TimetableCreate,
):
    user_id = payload.get("sub")
    timetable = await timetable_crud.create_timetable(
        session=session,
        timetable_create=timetable_create,
        user_id=user_id
    )
    return timetable


@router.get("/timetables", response_model=list[UserRead])
@cache(expire=30)
async def get_timetable(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    try:
        timetable = await timetable_crud.get_all_timetable(session=session)
        return timetable
    except Exception:
        return {"status": "error", "details": "Аn error occurred when forming a list of timetables"}


@router.get("/timetable/{timetable_id}/", response_model=UserRead)
@cache(expire=30)
async def get_timetable(
        session: Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        timetable_id: int
):
    try:
        timetable = await timetable_crud.get_timetable(session=session, timetable_id=timetable_id)

        return timetable
    except Exception:
        return {"status": "error", "details": "Schedule request error"}


@router.delete("/timetable/{timetable_id}/delete") #, status_code=status.HTTP_204_NO_CONTENT
async def delete_timetable(
        timetable: Timetable = Depends(timetable_by_id),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> None | dict:
    try:
        await timetable_crud.delete_timetable(session=session, timetable=timetable)
    except:
        return {"status": "error", "details": "Timetable deletion error"}
