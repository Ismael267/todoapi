from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Task(Base):
    task = Column(String, index=True)
    completed = Column(Boolean, default=False)
    dateOfRealisation = Column(DateTime)  # Changer le type de dateOfRealisation à <datetime>
    dateOfExecution = Column(DateTime, default=None)
    user_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="tasks")
  
    