# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from decimal import Decimal

class UserCreate(BaseModel):
    username: str
    password: str

class requestdetails(BaseModel):
    username: str
    password: str

class changepassword(BaseModel):
    username: str
    old_password: str
    new_password: str

class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime

# ----------------------------------------------------------   

class PhotoBase(BaseModel):
    title: str
    description: str
    price: float

class PhotoCreate(BaseModel):
    title: str
    description: str
    price: Optional[float] = None

class PhotoUpdate(BaseModel):
    title: str
    description: str
    price: Optional[float] = None

class Photo(PhotoBase):
    id_photo: int
    create_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True

class PhotoDetail(PhotoBase):
    id_photo: int
    id_author: int
    create_at: datetime
    update_at: datetime
    path: Optional[str] = None  
    
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

# ------------------------------------------------------
class PurchaseCreate(BaseModel):
    id_photo: int

class Purchase(BaseModel):
    id_purchase: int
    id_user: int
    id_photo: int
    amount: Decimal
    create_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
class PurchaseDetail(BaseModel):
    id_purchase: int
    id_user: int
    id_photo: int
    amount: Decimal
    create_at: datetime
    photo: PhotoDetail

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
