from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict


class UserLogin(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    access_token: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    pass


class UserUpdateAdmin(UserCreate):
    model_config = ConfigDict(
        from_attributes=True,
    )
    role: str
    is_active: bool
    is_verified: bool


class UserRead(UserUpdateAdmin):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime
    updated_at: datetime


class UserUpdatePartial(UserUpdate):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserUpdatePartialAdmin(UserUpdatePartial):
    role: str | None = None
    is_active: bool | None = None
    is_verified: bool | None = None


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
