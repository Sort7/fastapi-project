from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from authentication.auth import http_bearer
from core.config import settings
from core.models import db_helper, TrenerProfale
from core.schemas.trener import (
    ProfileTrenerRead, ProfileTrenerUpdatePartial, ProfileTrenerUpdate, ProfaleTrener)
from crud import trenet as trener_crud
from utils.check import check_admin
from utils.dependencies import trener_by_id
from utils.validate_token import get_current_token_payload

router = APIRouter(tags=["Treners"], prefix=settings.api.prefix, dependencies=[Depends(http_bearer)])


@router.post("/trener/{user_id}/create", response_model=ProfileTrenerRead)
async def create_profile_trener(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        create_trener_profile: ProfaleTrener,
        user_id: int,
):
    if check_admin(payload, role="admin") or (check_admin(payload, role="trener") and user_id == payload.get("sub")):
        profile_trener = await trener_crud.create_trener_profile(
            session=session,
            user_id=user_id,
            create_trener_profile=create_trener_profile,
        )
        return profile_trener

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.get("/trener/{trener_id}/", response_model=ProfileTrenerRead)
@cache(expire=30)
async def get_trener(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        trener_id: int
):
    trener_profile = await trener_crud.get_trener(session=session, trener_id=trener_id)
    return trener_profile


@router.get("/trener/{user_id}/profile")
async def get_trener_and_profile(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: int
):
    trener = await trener_crud.show_trener_and_profile(session=session, user_id=user_id)
    return trener


@router.get("/treners")
@cache(expire=30)
async def get_treners(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
):
    treners = await trener_crud.show_treners_with_profiles(session=session)
    return treners


@router.put("/trener/{trener_id}/update", response_model=ProfileTrenerRead)
async def update_user_profile_put(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        trener_profile: Annotated[TrenerProfale, Depends(trener_by_id)],
        trener_profile_update: ProfileTrenerUpdate,
):
    if check_admin(payload, role="admin") or trener_profile.__dict__.get("user_id") == payload.get("sub"):
        return await trener_crud.update_trener_profile(
            session=session,
            trener_profile=trener_profile,
            trener_profile_update=trener_profile_update,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.patch("/trener/{profile_id}/update", response_model=ProfileTrenerRead)
async def update_user_partial(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        trener_profile: Annotated[TrenerProfale, Depends(trener_by_id)],
        trener_profile_update: ProfileTrenerUpdatePartial,

):
    if check_admin(payload, role="admin") or trener_profile.__dict__.get("user_id") == payload.get("sub"):
        return await trener_crud.update_trener_profile(
            session=session,
            trener_profile=trener_profile,
            trener_profile_update=trener_profile_update,
            partial=True,
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )


@router.delete("/trener/{profile_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trener_profile(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        payload: Annotated[dict, Depends(get_current_token_payload)],
        trener_profile: Annotated[TrenerProfale, Depends(trener_by_id)],
) -> None:
    if check_admin(payload, role="admin") or trener_profile.__dict__.get("user_id") == payload.get("sub"):
        await trener_crud.delete_trener_profile(session=session, trener_profile=trener_profile)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"insufficient permissions to perform the operation",
    )
