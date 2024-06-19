from datetime import date

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

# from core.models.user import RolesProfile




class ProfileUser(BaseModel):
    name: str
    surname: str
    birthday: date | None = None

class ProfileAndUser(BaseModel):
    name: str
    surname: str
    birthday: date | None = None
    phone: str
    email: EmailStr


class ProfileUserCreate(ProfileUser):
    pass


class ProfileUserRead(ProfileUserCreate):

    id: int


class ProfileUserUpdate(ProfileUser):
    pass

class ProfileUserUpdatePartial(ProfileUserUpdate):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None


