from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any, Union
from decimal import Decimal

class ResponseBase(BaseModel):
    message: str
    data: Optional[Any] = None
    error: bool

class TokenResponseData(BaseModel):
    access_token: str
    refresh_token: str
    id_user: int

class UserListResponseData(BaseModel):
    id: int
    username: str
    create_at: datetime
    update_at: datetime

class UserResponseData(BaseModel):
    id: int
    username: str

class UserCreate(BaseModel):
    username: str
    password: str
    fullname: str
    contact: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserUpdate(BaseModel):
    fullname: Optional[str]
    contact: Optional[str]
    gender: Optional[str]
    address: Optional[str]
    photo_url: Optional[str]

class UserResponseData(BaseModel):
    id: int
    username: str
    fullname: str
    contact: str
    gender: Optional[str]
    address: Optional[str]
    photo_url: Optional[str]
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True

class changepassword(BaseModel):
    username: str
    old_password: str
    new_password: str

class TokenCreate(BaseModel):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime

# ----------------------------------------
class OrderStatusCreate(BaseModel):
    status_name: str

class OrderStatusUpdate(BaseModel):
    status_name: Optional[str]

class OrderStatusResponseData(BaseModel):
    status_id: int
    status_name: str
    class Config:
        orm_mode = True

# ---------------------------------------
class ItemCreate(BaseModel):
    item_name: str
    description: Optional[str]
    price_per_day: Decimal

class ItemUpdate(BaseModel):
    vendor_id: Optional[int]
    item_name: Optional[str]
    description: Optional[str]
    price_per_day: Optional[Decimal]
    image_url: Optional[str]

class ItemResponseData(BaseModel):
    item_id: int
    vendor_id: Optional[int]
    item_name: str
    description: Optional[str]
    price_per_day: Decimal
    image_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
# -----------------------------------------
class OrderCreate(BaseModel):
    user_id: Optional[int]
    item_id: Optional[int]
    status_id: Optional[int]
    order_date: Optional[datetime]
    return_date: Optional[datetime]
    total_price: Optional[Decimal]

class OrderUpdate(BaseModel):
    user_id: Optional[int]
    item_id: Optional[int]
    status_id: Optional[int]
    order_date: Optional[datetime]
    return_date: Optional[datetime]
    total_price: Optional[Decimal]

class OrderResponseData(BaseModel):
    order_id: int
    user_id: Optional[int]
    item_id: Optional[int]
    status_id: Optional[int]
    order_date: datetime
    return_date: Optional[datetime]
    total_price: Optional[Decimal]

    class Config:
        orm_mode = True
# ---------------------------------------
class VendorCreate(BaseModel):
    vendor_name: str
    email: str

class VendorUpdate(BaseModel):
    vendor_name: Optional[str]
    email: Optional[str]

class VendorResponseData(BaseModel):
    vendor_id: int
    vendor_name: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
# ----------------------------------------
class RatingCreate(BaseModel):
    order_id: Optional[int]
    user_id: Optional[int]
    item_id: Optional[int]
    rating: Optional[int]
    review: Optional[str]

class RatingUpdate(BaseModel):
    order_id: Optional[int]
    user_id: Optional[int]
    item_id: Optional[int]
    rating: Optional[int]
    review: Optional[str]

class RatingResponseData(BaseModel):
    rating_id: int
    order_id: Optional[int]
    user_id: Optional[int]
    item_id: Optional[int]
    rating: Optional[int]
    review: Optional[str]
    rating_date: datetime

    class Config:
        orm_mode = True

