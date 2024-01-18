from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Response(Base):
    
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String)
    token= Column(String,unique=True)
    # tasks = relationship("Task", back_populates="owner")
  
    