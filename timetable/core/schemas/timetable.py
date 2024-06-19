from datetime import date

from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

# from core.models.user import RolesProfile




class TimetableBase(BaseModel):
    data: date
    time: str
    user_profales_id: int
    trener_profales_id: int

# class TrenerAndUser(BaseModel):
#     name: str
#     surname: str
#     birthday: date | None = None
#     coaching_experience: float | None = None
#     sports_experience: float | None = None
#     education: str | None = None
#     specialization: str | None = None
#     biography: str | None = None


class TimetableCreate(TimetableBase):
    pass


class TimetableRead(TimetableCreate):

    id: int


# class ProfileTrenerUpdate(ProfaleTrener):
#     pass
#
# class ProfileTrenerUpdatePartial(ProfileTrenerUpdate):
#     name: str | None = None
#     surname: str | None = None
#     birthday: date | None = None
#     coaching_experience: float | None = None
#     sports_experience: float | None = None
#     education: str | None = None
#     specialization: str | None = None
#     biography: str | None = None