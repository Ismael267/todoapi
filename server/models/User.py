from sqlalchemy import  Column, String,Integer
from sqlalchemy.orm import relationship
from db.database import Base


class User(Base):
 
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    username = Column(String)
    tasks = relationship("Task", back_populates="owner")
   