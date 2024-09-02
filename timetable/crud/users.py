from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from authentication.utils import hash_password
from core.models import User
from core.schemas.user import UserCreate, UserBase, UserUpdateAdmin, UserUpdatePartialAdmin


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_token(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.scalars(stmt)
    user: User | None = result.one_or_none()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.scalars(stmt)
    user: User | None = result.one_or_none()
    return user


async def get_all_users(session: AsyncSession, ) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(session: AsyncSession, user_data: UserCreate, ) -> UserBase:
    password = hash_password(user_data.password)
    user = User(password=password, **user_data.model_dump(exclude={'password'}))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user: User,
        user_update: UserUpdateAdmin | UserUpdatePartialAdmin,
        partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial, exclude={'password'}).items():
        setattr(user, name, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(
        session: AsyncSession,
        user: User,
) -> None:
    await session.delete(user)
    await session.commit()
