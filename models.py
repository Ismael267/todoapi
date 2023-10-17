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
    # changer le type de  dateOfRealisation a <datetime>
    dateOfRealisation = Column(DateTime) 
    dateOfExecution= Column(DateTime,default=None)
    # creé un autre champ pour l'update de date  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
