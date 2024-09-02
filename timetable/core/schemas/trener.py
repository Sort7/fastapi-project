from datetime import date

from pydantic import BaseModel, EmailStr


class ProfaleTrener(BaseModel):
    name: str
    surname: str
    birthday: date | None = None
    coaching_experience: float | None = None
    sports_experience: float | None = None
    education: str | None = None
    specialization: str | None = None
    biography: str | None = None


class TrenerAndUser(ProfaleTrener):
    username: str
    password: bytes
    email: EmailStr | None = None


class ProfileTrenerCreate(ProfaleTrener):
    pass


class ProfileTrenerRead(ProfileTrenerCreate):
    id: int


class ProfileTrenerUpdate(ProfaleTrener):
    pass


class ProfileTrenerUpdatePartial(ProfileTrenerUpdate):
    name: str | None = None
    surname: str | None = None
    birthday: date | None = None
    coaching_experience: float | None = None
    sports_experience: float | None = None
    education: str | None = None
    specialization: str | None = None
    biography: str | None = None
