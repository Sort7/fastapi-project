from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload, load_only

from core.models import User, Post, UserProfale, TrenerProfale
from core.schemas.profile import ProfileUserUpdate, ProfileUserUpdatePartial, ProfileUserRead
from core.schemas.trener import ProfileTrenerUpdate, ProfileTrenerUpdatePartial


async def get_trener(session: AsyncSession, trener_id: int) -> TrenerProfale | None:
    return await session.get(TrenerProfale, trener_id)


async def create_trener_profile(
    session: AsyncSession,
    user_id: int,
    name: str,
    surname: str,
    birthday: date | None = None,
    coaching_experience: float | None = None,
    sports_experience: float | None = None,
    specialization: str | None = None,
    biography: str | None = None,
) -> TrenerProfale:
    profile_trener = TrenerProfale(
        user_id=user_id,
        name=name,
        surname=surname,
        birthday=birthday,
        coaching_experience=coaching_experience,
        sports_experience=sports_experience,
        specialization=specialization,
        biography=biography,
    )
    session.add(profile_trener)
    await session.commit()
    return profile_trener


async def show_treners_with_profiles(session: AsyncSession):
    stmt = (select(User).
            options(
            load_only(User.phone, User.email),
            joinedload(User.trener_profale).
                load_only(TrenerProfale.name, TrenerProfale.surname)
            ).
            order_by(User.id))
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    treners = await session.scalars(stmt)
    return treners.all()
    # for user in users:
    #     print(user)
    #     print(user.profile.first_name)


async def show_trener_and_profile(session: AsyncSession, user_id: int):
    stmt = (select(User).
            options(
            load_only(User.phone, User.email),
            joinedload(User.trener_profale).
                load_only(TrenerProfale.name, TrenerProfale.surname)
            ).
            where(User.id == user_id))
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    trener: User | None = await session.scalar(stmt)
    return trener
    # for user in users:
    #     print(user)
    #     print(user.profile.first_name)

async def update_trener_profile(
    session: AsyncSession,
    trener_profile:  TrenerProfale,
    trener_profile_update: ProfileTrenerUpdate | ProfileTrenerUpdatePartial,
    partial: bool = False,
) -> TrenerProfale:
    for name, value in trener_profile_update.model_dump(exclude_unset=partial).items():
        setattr(trener_profile, name, value)
    await session.commit()
    return trener_profile

