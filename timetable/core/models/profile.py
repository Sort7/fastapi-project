from typing import Optional
from datetime import date

from sqlalchemy import UniqueConstraint, Integer, String, ForeignKey, Boolean, func, Date, Float,Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from core.models import Base, User


class UserProfale(Base):
    __tablename__ = "user_profales"

    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String, nullable=False
    )
    birthday: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True, unique=False
    )
    user: Mapped["User"] = relationship(back_populates="user_profale")
    user_records: Mapped[list["Timetable"]] = relationship(back_populates="user_profale")


class TrenerProfale(Base):
    __tablename__ = "trener_profales"

    name: Mapped[str] = mapped_column(
        String, nullable=False
    )
    surname: Mapped[str] = mapped_column(
        String, nullable=False
    )
    birthday: Mapped[str | None] = mapped_column(
        Date, nullable=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True, unique=False
    )
    coaching_experience: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    sports_experience: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )
    education: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    specialization: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    biography: Mapped[str | None] = mapped_column(
        Text, default="",  server_default=""
    )
    user: Mapped["User"] = relationship(back_populates="trener_profale")
    trener_records: Mapped[list["Timetable"]] = relationship(back_populates="trener_profale")