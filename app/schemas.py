from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    id: int
    created_at: datetime
    owner_data: UserOutput

    class Config:
        orm_mode = True
