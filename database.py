from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


URL_DATABASE = 'postgresql://totoaazerty:gzJmUGpq.u89gKQ@postgresql-totoaazerty.alwaysdata.net/totoaazerty_azerty'

try:
    engine = create_engine(URL_DATABASE)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    print(f"An error occurred: {str(e)}")
