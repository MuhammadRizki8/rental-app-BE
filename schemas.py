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
    
# ----------------------------------------------------------   
    
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
    create_at: datetime
    update_at: datetime
    
# -------------------------------------------------------
class WalletBase(BaseModel):
    id_user: int
    balance: float

class WalletCreate(WalletBase):
    pass

class WalletUpdate(WalletBase):
    pass

class Wallet(WalletBase):
    id_wallet: int
    create_at: Optional[str]
    update_at: Optional[str]