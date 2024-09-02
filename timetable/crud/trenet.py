from datetime import date
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload, load_only

from core.models import User, UserProfale, TrenerProfale
from core.schemas.profile import ProfileUserUpdate, ProfileUserUpdatePartial, ProfileUserRead
from core.schemas.trener import ProfileTrenerUpdate, ProfileTrenerUpdatePartial, ProfaleTrener


async def get_trener(session: AsyncSession, trener_id: int) -> TrenerProfale | None:
    trener = await session.get(TrenerProfale, trener_id)
    return trener


async def create_trener_profile(
        session: AsyncSession,
        create_trener_profile: ProfaleTrener,
        user_id: int,
) -> TrenerProfale:
    profile_trener = TrenerProfale(user_id=user_id, **create_trener_profile.model_dump())
    session.add(profile_trener)
    await session.commit()
    return profile_trener


async def show_treners_with_profiles(session: AsyncSession):
    stmt = (select(User).
            options(
        load_only(User.username, User.email),
        joinedload(User.trener_profale)
    ).
            order_by(User.id))
    treners = await session.scalars(stmt)
    return treners.all()


async def show_trener_and_profile(session: AsyncSession, user_id: int):
    stmt = (select(User).
            options(
        load_only(User.username, User.email),
        joinedload(User.trener_profale)
    ).
            where(User.id == user_id))
    trener: User | None = await session.scalar(stmt)
    return trener


async def update_trener_profile(
        session: AsyncSession,
        trener_profile: TrenerProfale,
        trener_profile_update: ProfileTrenerUpdate | ProfileTrenerUpdatePartial,
        partial: bool = False,
) -> TrenerProfale:
    for name, value in trener_profile_update.model_dump(exclude_unset=partial).items():
        setattr(trener_profile, name, value)
    await session.commit()
    return trener_profile



async def delete_trener_profile(
        session: AsyncSession,
        trener_profile: TrenerProfale,
) -> None:
    await session.delete(trener_profile)
    await session.commit()