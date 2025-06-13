from pydantic import BaseModel, Field
from typing import Optional
import datetime
import uuid

class EventBase(BaseModel):
    title: str
    location: str
    date: datetime.date
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
class EventCreate(EventBase):
    pass

class Event(EventBase):
    is_open: bool = True
    
    class Config:
        form_attribute =True

class EventUpdate(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime.date] = None
    is_open: Optional[bool] = None
    
