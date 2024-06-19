from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import UniqueConstraint, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from .base import Base
# from .mixins.int_id_pk import IntIdPkMixin

class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(
        String(length=320), nullable=False
    )
    text: Mapped[str] = mapped_column(
        String(), nullable=False
    )

