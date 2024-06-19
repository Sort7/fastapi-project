from datetime import date
from typing import Annotated

from fastapi import APIRouter,Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper, User, UserProfale, TrenerProfale
from core.schemas.post import PostRead
from core.schemas.profile import ProfileUserRead, ProfileAndUser, ProfileUserUpdatePartial, ProfileUserUpdate
from core.schemas.trener import ProfileTrenerRead, ProfileTrenerUpdatePartial, ProfileTrenerUpdate
from core.schemas.user import UserRead, UserCreate, UserUpdate, UserUpdatePartial
from crud import trenet as trener_crud
from utils.dependencies import trener_by_id

router = APIRouter(tags=["Treners"], prefix=settings.api.prefix,)



@router.get("/trener/{trener_id}/", response_model=ProfileTrenerRead)
async def get_trener(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        trener_id: int
):
    trener_profile = await trener_crud.get_trener(session=session, trener_id=trener_id)

    return trener_profile





@router.post("/trener/{user_id}/profile", response_model=ProfileTrenerRead)
async def create_profile_trener(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    user_id: int,
    name: str,
    surname: str,
    birthday: date | None = None,
    coaching_experience: float | None = None,
    sports_experience: float | None = None,
    specialization: str | None = None,
    biography: str | None = None,
):
    profile_trener = await trener_crud.create_trener_profile(
        session=session,
        user_id=user_id,
        name=name,
        surname=surname,
        birthday=birthday,
        coaching_experience=coaching_experience,
        sports_experience=sports_experience,
        specialization=specialization,
        biography=biography,
    )
    return profile_trener
#



@router.get("/treners")
async def get_treners(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    treners = await trener_crud.show_treners_with_profiles(session=session)
    return treners

@router.get("/trener/{user_id}/profile")
async def get_trener_and_profile(
        session:  Annotated[
            AsyncSession, Depends(db_helper.session_getter),
        ],
        user_id: int
):
    trener = await trener_crud.show_trener_and_profile(session=session, user_id=user_id)

    return trener


@router.put("/trener/{trener_id}/update")
async def update_user_profile_put(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trener_profile: Annotated[TrenerProfale, Depends(trener_by_id)],
    trener_profile_update: ProfileTrenerUpdate,
    ):
    return await trener_crud.update_trener_profile(
        session=session,
        trener_profile=trener_profile,
        trener_profile_update=trener_profile_update,
    )


@router.patch("/trener/{profile_id}/update")
async def update_user_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    trener_profile: Annotated[TrenerProfale, Depends(trener_by_id)],
    trener_profile_update: ProfileTrenerUpdatePartial,
):
    return await trener_crud.update_trener_profile(
        session=session,
        trener_profile=trener_profile,
        trener_profile_update=trener_profile_update,
        partial=True,
    )

