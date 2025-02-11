from sqlalchemy import Column, Integer, String
from ..connection import Base, session
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    products = relationship("Product", back_populates="category")
    
    def find_all():
        try:
            response = session.query(Category).all()
            return response
        except Exception as e:
            return e
        finally:
            session.close()


    def find_by_filter(**kwargs):
        try:
            response = session.query(Category).filter_by(**kwargs).first()
            return response
        except Exception as e:
            return e
        finally:
            session.close()




