from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Timetable
from core.schemas.timetable import TimetableCreate


async def get_timetable(session: AsyncSession, timetable_id: int) -> Timetable | None:
    return await session.get(Timetable, timetable_id)


async def get_all_timetable(
        session: AsyncSession,
) -> list[Timetable]:
    stmt = select(Timetable).order_by(Timetable.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_timetable(session: AsyncSession, timetable_create: TimetableCreate, user_id: int) -> Timetable:
    trener = timetable_create.__dict__.get("trener_profales_id")
    print(trener)
    if trener is not None:
        timetable = Timetable(user_id=user_id, **timetable_create.model_dump())
        session.add(timetable)
        await session.commit()
        await session.refresh(timetable)
        return timetable

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"trainer not found",
    )


async def delete_timetable(
        session: AsyncSession,
        timetable: Timetable,
) -> None:
    await session.delete(timetable)
    await session.commit()
