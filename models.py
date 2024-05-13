from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Photo(Base):
    __tablename__ = "photo"
    id_photo = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, unique=True)
    id_author = Column(Integer, ForeignKey("user.id"))
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    

class Wallet(Base):
    __tablename__ = "wallet"
    id_wallet = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("user.id"))
    balance = Column(DECIMAL(10, 2), nullable=False)
    create_at = Column(DateTime, nullable=False, default=datetime.now)
    update_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)