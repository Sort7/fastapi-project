from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Post, Timetable
from core.schemas.timetable import TimetableCreate
from core.schemas.user import UserCreate, UserUpdate, UserUpdatePartial, UserRead
from core.schemas.post import PostCreate

async def get_all_timetable(
    session: AsyncSession,
) -> list[Timetable]:
    stmt = select(Timetable).order_by(Timetable.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_timetable(session: AsyncSession, timetable_id: int) -> Timetable | None:
    return await session.get(Timetable, timetable_id)


async def create_timetable(
    session: AsyncSession,
    timetable_create: TimetableCreate,
) -> Timetable:
    timetable = Timetable(**timetable_create.model_dump())
    session.add(timetable)
    await session.commit()
    await session.refresh(timetable)
    return timetable


async def delete_timetable(
    session: AsyncSession,
    timetable: Timetable,
) -> None:
    await session.delete(timetable)
    await session.commit()