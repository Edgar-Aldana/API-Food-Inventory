from fastapi.logger import logger
from sqlalchemy import Column, Integer, String
from ..connection import Base, session

class User(Base):
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def find_by_filter(**kwargs):
        try:
            return session.query(User).filter_by(**kwargs).first()
        except Exception as e:
            return e
        finally:
            session.close()
        