from datetime import datetime

from sqlalchemy import MetaData, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=func.now(),
    )