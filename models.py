from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Nullable, String, TIMESTAMP, DECIMAL, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy import Table,DateTime
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
    title = Column(String(255), index=True,unique=True)
    id_author = Column(Integer, ForeignKey("user.id"))
    description = Column(Text)
    price = Column(DECIMAL(10, 2))
    create_at = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP')
    update_at = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
