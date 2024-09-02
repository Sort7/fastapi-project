from typing import Optional
from datetime import date, time, datetime

from sqlalchemy import UniqueConstraint, Integer, String, ForeignKey, Boolean, func, Date, Float, Time, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from core.models import Base, User


class Timetable(Base):
    __tablename__ = "timetables"

    recording_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )
    recording_time: Mapped[str] = mapped_column(
        String, nullable=False
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    trener_profales_id: Mapped[int | None] = mapped_column(
        ForeignKey("trener_profales.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="user_records")
    trener_profale: Mapped["TrenerProfale"] = relationship(back_populates="trener_records")
