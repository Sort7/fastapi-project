from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from core.models import db_helper, User, UserProfale, TrenerProfale, Timetable
from crud.profile import get_profile
from crud.timetable import get_timetable
from crud.trenet import get_trener
from crud.users import get_user
from utils.validate_token import get_current_token_payload


async def user_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await get_user(session=session, user_id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )

async def user_by_payload(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    session: AsyncSession = Depends(db_helper.session_getter),

) -> User:
    user_id = payload.get("sub")
    user = await get_user(session=session, user_id=user_id)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found!",
    )


async def user_profile_by_id(
    profile_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserProfale:
    user_profile = await get_profile(session=session, profile_id=profile_id)
    if user_profile is not None:
        return user_profile

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Profile {profile_id} not found!",
    )

async def trener_by_id(
    trener_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TrenerProfale:
    trener_profile = await get_trener(session=session, trener_id=trener_id)
    if trener_profile is not None:
        return trener_profile

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trener {trener_id} not found!",
    )

async def timetable_by_id(
    timetable_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Timetable:
    timetable = await get_timetable(session=session, timetable_id=timetable_id)
    if timetable is not None:
        return timetable

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Timetable {timetable_id} not found!",
    )

