import sqlalchemy as db
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

engine = db.create_engine('sqlite:///database.db', echo=True)

# Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))
session = Session()