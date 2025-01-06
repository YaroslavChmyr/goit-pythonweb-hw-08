from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[datetime] = None
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True  # Updated from 'orm_mode'

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[datetime]
    additional_info: Optional[str]

    class Config:
        from_attributes = True

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True