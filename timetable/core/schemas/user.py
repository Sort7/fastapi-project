from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

# from core.models.user import RolesProfile


class PostBase(BaseModel):
    username: str

class UserBase_1(BaseModel):
    id: int
    phone: str
    email: EmailStr
    hashed_password: str


class UserCreate(UserBase):
    pass

class UserCreate_1(UserBase_1):
    pass


class UserRead(UserBase):
    # model_config = ConfigDict(
    #     from_attributes=True,
    # )

    id: int

class UserRead_1(UserBase_1):
    # model_config = ConfigDict(
    #     from_attributes=True,
    # )

    id: int
    is_superuser: bool
    role_profile: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime



