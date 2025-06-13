from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid 

class UserBase(BaseModel):
    name: str
    email: EmailStr
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
class UserCreate(UserBase): #inherits from UserBase
    pass

class User(UserBase): #inherits from UserBase
    is_active: bool = True

    class Config:
        form_attribute = True

class UserUpdate(BaseModel): 
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

