from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
import uuid

class SpeakerBase(BaseModel):
    name: str
    topic: str
    

class Speaker(SpeakerBase):
    pass

class Speaker(SpeakerBase):
    id: str = Field(str(uuid.uuid4()))
    
    class Config:
        form_attribute = True

class SpeakerUpdate(BaseModel):
    name: Optional[str] = None
    topic: Optional[str] = None