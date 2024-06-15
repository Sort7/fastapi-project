from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

# from core.models.user import RolesProfile


class PostBase(BaseModel):
    title: str
    text: str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    # model_config = ConfigDict(
    #     from_attributes=True,
    # )

    id: int
