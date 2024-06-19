from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Post
from core.schemas.user import UserCreate, UserUpdate, UserUpdatePartial, UserRead
from core.schemas.post import PostCreate

async def get_all_users(
    session: AsyncSession,
) -> list[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_all_post(
    session: AsyncSession,
) -> list[Post]:
    stmt = select(Post).order_by(Post.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_post(
    session: AsyncSession,
    user_create: PostCreate,
) -> Post:
    post = Post(**user_create.model_dump())
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def update_user(
    session: AsyncSession,
    user: UserRead,
    user_update: UserUpdate | UserUpdatePartial,
    partial: bool = False,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
