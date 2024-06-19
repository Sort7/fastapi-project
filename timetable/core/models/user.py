from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import UniqueConstraint, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base
# from .mixins.int_id_pk import IntIdPkMixin

class Roles(Enum):
    admin = "admin"
    manager = "manager"
    trener = "trener"
    user = "user"

class User(Base):
    __tablename__ = "users"

    phone: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    role: Mapped[Roles] = mapped_column(
        default="user", server_default="user", nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    user_profale: Mapped["UserProfale"] = relationship(back_populates="user")
    trener_profale: Mapped["TrenerProfale"] = relationship(back_populates="user")
