from datetime import date
from typing import Annotated

from fastapi import APIRouter,Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User, UserProfale
from core.schemas.profile import ProfileUserRead, ProfileAndUser, ProfileUserUpdatePartial, ProfileUserUpdate
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import profile as profile_crud
from crud.users import update_user
from utils.dependencies import user_by_id, user_profile_by_id

router = APIRouter(tags=["Profales"], prefix=settings.api.prefix,)


@router.get("/profiles")
async def get_profiles(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    try:
        profiles = await profile_crud.show_users_with_profiles(session=session)
        return profiles
    except Exception:
        return {"status": "error", "details": "Аn error occurred when forming a list of user profiles"}

@router.get("/profile/{user_id}/profile")
async def get_user_and_profile(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        user_id: int
):
    try:
        user = await profile_crud.show_user_and_profile(session=session, user_id=user_id)

        return user
    except Exception:
        return {"status": "error", "details": "Аn error occurred when forming a list of profiles users"}

@router.get("/profile/{profile_id}/", response_model=ProfileUserRead)
async def get_profile(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        profile_id: int
):
    try:
        user_profile = await profile_crud.get_profile(session=session, profile_id=profile_id)

        return user_profile
    except Exception:
        return {"status": "error", "details": "User profile creation error"}

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
    try:
        profile_user = await profile_crud.create_user_profile(
            session=session,
            user_id=user_id,
            name=name,
            surname=surname,
            birthday=birthday,
        )
        return profile_user
    except Exception:
        return {"status": "error", "details": "Error when creating a user profile"}

@router.put("/profile/{profile_id}/update")
async def update_user_profile_put(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
    user_profile_update: ProfileUserUpdate,
    ):
    try:
        return await profile_crud.update_user_profile(
            session=session,
            user_profile=user_profile,
            user_profile_update=user_profile_update,
        )
    except Exception:
        return {"status": "error", "details": "Error updating the user profile by the method - put"}


@router.patch("/profile/{profile_id}/update")
async def update_user_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
    user_profile_update: ProfileUserUpdatePartial,
):
    try:
        return await profile_crud.update_user_profile(
            session=session,
            user_profile=user_profile,
            user_profile_update=user_profile_update,
            partial=True,
        )
    except Exception:
        return {"status": "error", "details": "Error updating the user profile by the method - patch"}

