from typing import Optional

from sqlalchemy import UniqueConstraint, Integer, String, ForeignKey, Boolean, func, Date, Float
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from core.models import Base, User




class Timetable(Base):
    __tablename__ = "timetables"

    data: Mapped[Date] = mapped_column(
        Date, nullable=False
    )
    time: Mapped[str] = mapped_column(
        String, nullable=False
    )
    user_profales_id: Mapped[int | None] = mapped_column(
        ForeignKey("user_profales.id", ondelete="CASCADE"), nullable=True
    )
    trener_profales_id: Mapped[int | None] = mapped_column(
        ForeignKey("trener_profales.id", ondelete="CASCADE"), nullable=True
    )
    user_profale: Mapped["UserProfale"] = relationship(back_populates="user_records")
    trener_profale: Mapped["TrenerProfale"] = relationship(back_populates="trener_records")