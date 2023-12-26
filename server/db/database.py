from sqlalchemy import create_engine, Integer, Column, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import as_declarative,declared_attr
from core.settings import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
engine = create_engine(settings.get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
