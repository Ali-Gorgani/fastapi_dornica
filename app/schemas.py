from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    userName: str
    fullName: Optional[str] = None
    email: EmailStr
    password: str
    DoB: Optional[str] = None
    gender: Optional[str] = "NOT_SPECIFIED"


class UserOut(BaseModel):
    id: int
    userName: str
    fullName: Optional[str] = None
    email: EmailStr
    DoB: Optional[str] = None
    gender: Optional[str] = "NOT_SPECIFIED"
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ListingCreate(BaseModel):
    type: str
    availableNow: Optional[bool] = True
    address: str


class ListingOut(BaseModel):
    id: int
    type: str
    availableNow: Optional[bool] = True
    address: str
    createdAt: datetime
    updatedAt: datetime
    owner: UserOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
