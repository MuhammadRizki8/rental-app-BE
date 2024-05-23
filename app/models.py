# models.py
from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import BaseDB
from datetime import datetime

class User(BaseDB):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    photos = relationship("Photo", back_populates="author")
    wallets = relationship("Wallet", back_populates="user")
    purchases = relationship("Purchase", back_populates="user")
    tokens = relationship("TokenTable", back_populates="user")

class TokenTable(BaseDB):
    __tablename__ = "token"
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="tokens")

class Photo(BaseDB):
    __tablename__ = "photo"
    id_photo = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, unique=True)
    id_author = Column(Integer, ForeignKey("user.id"),  nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    path = Column(String(255), nullable=True)  # Tambahkan kolom ini

    author = relationship("User", back_populates="photos")
    purchases = relationship("Purchase", back_populates="photo")

class Wallet(BaseDB):
    __tablename__ = "wallet"
    id_wallet = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    balance = Column(DECIMAL(10, 2), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="wallets")

class Purchase(BaseDB):
    __tablename__ = "purchase"
    id_purchase = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id"), nullable=False)
    id_photo = Column(Integer, ForeignKey("photo.id_photo"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="purchases")
    photo = relationship("Photo", back_populates="purchases")
