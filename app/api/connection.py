from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from os import getenv



load_dotenv()


DATABASE_NAME = getenv("DATABASE_NAME")
DATABASE_URL = f"sqlite:///./api/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()



