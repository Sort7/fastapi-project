from typing import Annotated

from fastapi import APIRouter,Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User, Timetable
from core.schemas.post import PostRead
from core.schemas.timetable import TimetableRead, TimetableCreate
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import users as users_crud
from crud import timetable as timetable_crud
from utils.dependencies import user_by_id, timetable_by_id

router = APIRouter(tags=["Tametable"], prefix=settings.api.prefix,)


@router.get("/timetables", response_model=list[UserRead])
async def get_timetable(
    # session: AsyncSession = Depends(db_helper.session_getter),
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    timetable = await timetable_crud.get_all_timetable(session=session)
    return timetable


@router.get("/timetable/{timetable_id}/", response_model=UserRead)
async def get_timetable(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        timetable_id: int
):
    timetable = await users_crud.get_timetable(session=session, user_id=timetable_id)

    return timetable


@router.post("/timetable/create", response_model=TimetableRead)
async def create_timetable(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    timetable_create: TimetableCreate,
):
    user = await timetable_crud.create_timetable(
        session=session,
        timetable_create=timetable_create,
    )
    return user


@router.delete("/timetable/{timetable_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timetable(
    timetable: Timetable = Depends(timetable_by_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    await timetable_crud.delete_timetable(session=session, timetable=timetable)
