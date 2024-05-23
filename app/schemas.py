# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any
from decimal import Decimal

class ResponseBase(BaseModel):
    message: str
    data: Optional[Any] = None
    error: bool
    
class UserResponseData(BaseModel):
    id: int
    username: str
    id_wallet: Optional[int] = None

class TokenResponseData(BaseModel):
    access_token: str
    refresh_token: str
    id_user: int
    id_wallet: int

class UserListResponseData(BaseModel):
    id: int
    username: str
    create_at: datetime
    update_at: datetime
    
class PhotoDetailResponseData(BaseModel):
    id_photo: int
    id_author: int
    title: str
    description: str
    price: float
    create_at: datetime
    update_at: datetime
    path: Optional[str] = None 

class PasswordChangeResponseData(BaseModel):
    pass 
# ----------------------------------------------------------

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
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
