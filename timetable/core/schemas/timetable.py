from datetime import date

from pydantic import BaseModel


class TimetableBase(BaseModel):
    recording_date: date
    recording_time: str
    trener_profales_id: int


class TimetableCreate(TimetableBase):
    pass


class TimetableRead(TimetableCreate):
    id: int

