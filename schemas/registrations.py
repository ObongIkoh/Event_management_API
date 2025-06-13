from pydantic import BaseModel, Field
from datetime import date
from uuid import UUID, uuid4
from typing import Optional

class RegistrationBase(BaseModel):
    user_id: int
    event_id: int

class RegistrationCreate(RegistrationBase):
    pass

class Registration(RegistrationBase):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    registration_date: date = Field(default_factory=date.today)
    attended: bool = False

    class Config:
       form_attribute =True

class RegistrationUpdate(BaseModel):
    user_id: Optional[int] = None
    event_id: Optional[int] = None
    registration_date: Optional[date] = None
    attended: Optional[bool] = None