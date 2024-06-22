from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from .database import BaseDB
from datetime import datetime

class User(BaseDB):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    gender = Column(Enum('Pria', 'Wanita', name="gender_enum"), nullable=True)
    address = Column(String, nullable=True)  # New field for address
    photo_url = Column(String, nullable=True)  # New field for profile photo URL
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    tokens = relationship("TokenTable", back_populates="user")
    orders = relationship("Order", back_populates="user")
    ratings = relationship("Rating", back_populates="user")


# TokenTable
class TokenTable(BaseDB):
    __tablename__ = "token"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="tokens")

class Vendor(BaseDB):
    __tablename__ = "vendors"
    vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    items = relationship("Item", back_populates="vendor")

class Item(BaseDB):
    __tablename__ = "items"
    item_id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"), nullable=True)
    item_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price_per_day = Column(DECIMAL(10, 2), nullable=False)
    image_url = Column(String(255), nullable=True)  # New column for the image URL
    created_at = Column(DateTime, default=datetime.now)

    vendor = relationship("Vendor", back_populates="items")
    orders = relationship("Order", back_populates="item")
    ratings = relationship("Rating", back_populates="item")

class OrderStatus(BaseDB):
    __tablename__ = "order_status"
    status_id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="status")

class Order(BaseDB):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=True)
    status_id = Column(Integer, ForeignKey("order_status.status_id"), nullable=True)
    order_date = Column(DateTime, default=datetime.now)
    return_date = Column(DateTime, nullable=True)
    total_price = Column(DECIMAL(10, 2), nullable=True)

    user = relationship("User", back_populates="orders")
    item = relationship("Item", back_populates="orders")
    status = relationship("OrderStatus", back_populates="orders")
    ratings = relationship("Rating", back_populates="order")

class Rating(BaseDB):
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=True)
    rating = Column(Integer, nullable=True)
    review = Column(Text, nullable=True)
    rating_date = Column(DateTime, default=datetime.now)

    order = relationship("Order", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
    item = relationship("Item", back_populates="ratings")