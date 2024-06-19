from datetime import date
from typing import Annotated

from fastapi import APIRouter,Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User, UserProfale
from core.schemas.post import PostRead
from core.schemas.profile import ProfileUserRead, ProfileAndUser, ProfileUserUpdatePartial, ProfileUserUpdate
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import profile as profile_crud
from crud.users import update_user
from utils.dependencies import user_by_id, user_profile_by_id

router = APIRouter(tags=["Profales"], prefix=settings.api.prefix,)


@router.post("/profile/{user_id}/profile", response_model=ProfileUserRead)
async def create_profile_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_id: int,
    name: str,
    surname: str,
    birthday: date,
):
    profile_user = await profile_crud.create_user_profile(
        session=session,
        user_id=user_id,
        name=name,
        surname=surname,
        birthday=birthday,
    )
    return profile_user

@router.get("/profiles")
async def get_profiles(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    users = await profile_crud.show_users_with_profiles(session=session)
    return users

@router.get("/profile/{user_id}/profile")
async def get_user_and_profile(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        user_id: int
):
    user = await profile_crud.show_user_and_profile(session=session, user_id=user_id)

    return user


@router.get("/profile/{profile_id}/", response_model=ProfileUserRead)
async def get_profile(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        profile_id: int
):
    user_profile = await profile_crud.get_profile(session=session, profile_id=profile_id)

    return user_profile


@router.put("/profile/{profile_id}/update")
async def update_user_profile_put(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
    user_profile_update: ProfileUserUpdate,
    ):
    return await profile_crud.update_user_profile(
        session=session,
        user_profile=user_profile,
        user_profile_update=user_profile_update,
    )


@router.patch("/profile/{profile_id}/update")
async def update_user_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
    user_profile_update: ProfileUserUpdatePartial,
):
    return await profile_crud.update_user_profile(
        session=session,
        user_profile=user_profile,
        user_profile_update=user_profile_update,
        partial=True,
    )

