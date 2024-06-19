from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

# from core.models.user import RolesProfile




class UserBase(BaseModel):
    phone: str
    email: EmailStr
    hashed_password: str

class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    # model_config = ConfigDict(
    #     from_attributes=True,
    # )

    id: int
    is_superuser: bool
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

class UserUpdate(UserBase):
    pass

class UserUpdatePartial(UserUpdate):
    phone: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None




class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True



