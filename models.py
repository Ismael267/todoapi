from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime  
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Task(Base):
    __tablename__ = "tasks"  

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)
    completed = Column(Boolean, default=False)
    dateOfRealisation = Column(String, index=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
