from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserAuth(UserBase):
    password: str

class User(UserBase):
    id: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
    
class PhotoBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class Photo(PhotoBase):
    id_photo: int
    id_author: int

    class Config:
        orm_mode = True
