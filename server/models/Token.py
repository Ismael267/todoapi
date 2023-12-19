from sqlalchemy import Boolean, Column, DateTime, String, Integer, ForeignKey
from datetime import datetime
from db.database import Base

class Token(Base):
    
    user_id = Column(Integer, ForeignKey("user.id"))
    access_token = Column(String, unique=True, index=True)
    refresh_token = Column(String, nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.now)
    