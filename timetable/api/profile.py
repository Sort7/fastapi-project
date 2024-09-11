from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from authentication.utils import http_bearer
from core.config import settings
from core.models import db_helper, UserProfale
from core.schemas.profile import ProfileUserRead, ProfileUserUpdatePartial, ProfileUserUpdate, \
    ProfileUserCreate
from crud import profile as profile_crud
from utils.check import check_admin
from utils.dependencies import user_profile_by_id
from utils.validate_token import get_current_token_payload

router = APIRouter(tags=["Profales"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.post("/profile/{user_id}/profile", response_model=ProfileUserRead)
async def create_profile_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        create_user_profile: ProfileUserCreate,
        user_id: int,
):
    if check_admin(payload, role="admin") or user_id == payload.get("sub"):
        profile_user = await profile_crud.create_user_profile(
            session=session,
            user_id=user_id,
            create_user_profile=create_user_profile,
        )
        return profile_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.get("/profiles")
@cache(expire=30)
async def get_profiles(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
):
    if check_admin(payload, role="admin"):
        profiles = await profile_crud.show_users_with_profiles(session=session)
        return profiles

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation"
    )


@router.get("/profile/{user_id}/profile")
@cache(expire=30)
async def get_user_and_profile(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: int
):
    if check_admin(payload, role="admin") or user_id == payload.get("sub"):
        user = await profile_crud.show_user_and_profile(session=session, user_id=user_id)
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation"
    )


@router.get("/profile/{profile_id}/", response_model=ProfileUserRead)
@cache(expire=30)
async def get_profile(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        profile_id: int
):
    user_profile = await profile_crud.get_profile(session=session, profile_id=profile_id)
    return user_profile


@router.put("/profile/{profile_id}/update")
async def update_user_profile_put(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
        user_profile_update: ProfileUserUpdate,
):
    if check_admin(payload, role="admin") or user_profile.__dict__.get("user_id") == payload.get("sub"):
        return await profile_crud.update_user_profile(
            session=session,
            user_profile=user_profile,
            user_profile_update=user_profile_update,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.patch("/profile/{profile_id}/update")
async def update_user_partial(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
        user_profile_update: ProfileUserUpdatePartial,
):
    if check_admin(payload, role="admin") or user_profile.__dict__.get("user_id") == payload.get("sub"):
        return await profile_crud.update_user_profile(
            session=session,
            user_profile=user_profile,
            user_profile_update=user_profile_update,
            partial=True,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.delete("/profile/{profile_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_profile(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_profile: Annotated[UserProfale, Depends(user_profile_by_id)],
) -> None:
    if check_admin(payload, role="admin") or user_profile.__dict__.get("user_id") == payload.get("sub"):
        await profile_crud.delete_user_profile(session=session, user_profile=user_profile)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )
