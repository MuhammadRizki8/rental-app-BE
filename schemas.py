from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class requestdetails(BaseModel):
    username:str
    password:str

class changepassword(BaseModel):
    username:str
    old_password:str
    new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime
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
    
    class Config:
        from_attributes = True
    
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
    
    class Config:
        from_attributes = True