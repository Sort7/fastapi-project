from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, subqueryload, load_only

from core.models import User, Post, UserProfale
from core.schemas.profile import ProfileUserUpdate, ProfileUserUpdatePartial, ProfileUserRead



async def get_profile(session: AsyncSession, profile_id: int) -> UserProfale | None:
    return await session.get(UserProfale, profile_id)


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    name: str,
    surname: str,
    birthday: date | None = None,
) -> UserProfale:
    profile_user = UserProfale(
        user_id=user_id,
        name=name,
        surname=surname,
        birthday=birthday,
    )
    session.add(profile_user)
    await session.commit()
    return profile_user


async def show_users_with_profiles(session: AsyncSession):
    stmt = (select(User).
            options(
            load_only(User.phone, User.email),
            joinedload(User.user_profale).
                load_only(UserProfale.name, UserProfale.surname)
            ).
            order_by(User.id))
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    users = await session.scalars(stmt)
    return users.all()
    # for user in users:
    #     print(user)
    #     print(user.profile.first_name)


async def show_user_and_profile(session: AsyncSession, user_id: int):
    stmt = (select(User).
            options(
            load_only(User.phone, User.email),
            joinedload(User.user_profale).
                load_only(UserProfale.name, UserProfale.surname)
            ).
            where(User.id == user_id))
    # result: Result = await session.execute(stmt)
    # users = result.scalars()
    user: User | None = await session.scalar(stmt)
    return user
    # for user in users:
    #     print(user)
    #     print(user.profile.first_name)

async def update_user_profile(
    session: AsyncSession,
    user_profile:  UserProfale,
    user_profile_update: ProfileUserUpdate | ProfileUserUpdatePartial,
    partial: bool = False,
) -> UserProfale:
    for name, value in user_profile_update.model_dump(exclude_unset=partial).items():
        setattr(user_profile, name, value)
    await session.commit()
    return user_profile

