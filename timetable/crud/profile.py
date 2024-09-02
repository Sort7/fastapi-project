from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only

from core.models import User, UserProfale
from core.schemas.profile import ProfileUserUpdate, ProfileUserUpdatePartial, ProfileUserCreate


async def get_profile(session: AsyncSession, profile_id: int) -> UserProfale | None:
    profile = await session.get(UserProfale, profile_id)
    if profile:
        return profile

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Profile {profile_id} not found!",
    )


async def create_user_profile(
        session: AsyncSession,
        create_user_profile: ProfileUserCreate,
        user_id: int,
) -> UserProfale:
    profile_user = UserProfale(user_id=user_id, **create_user_profile.model_dump())
    session.add(profile_user)
    await session.commit()
    return profile_user


async def show_users_with_profiles(session: AsyncSession):
    stmt = (select(User).
            options(
        load_only(User.username, User.email),
        joinedload(User.user_profale)
    ).
            order_by(User.id))
    users = await session.scalars(stmt)
    return users.all()


async def show_user_and_profile(session: AsyncSession, user_id: int):
    stmt = (select(User).
            options(
        load_only(User.username, User.email),
        joinedload(User.user_profale).
        load_only(UserProfale.name, UserProfale.surname, UserProfale.birthday)
    ).
            where(User.id == user_id))
    user: User | None = await session.scalar(stmt)
    return user


async def update_user_profile(
        session: AsyncSession,
        user_profile: UserProfale,
        user_profile_update: ProfileUserUpdate | ProfileUserUpdatePartial,
        partial: bool = False,
) -> UserProfale:
    for name, value in user_profile_update.model_dump(exclude_unset=partial).items():
        setattr(user_profile, name, value)
    await session.commit()
    return user_profile


async def delete_user_profile(
        session: AsyncSession,
        user_profile: UserProfale,
) -> None:
    await session.delete(user_profile)
    await session.commit()
