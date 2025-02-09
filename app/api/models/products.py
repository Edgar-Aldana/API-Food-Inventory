from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..connection import session, Base
from sqlalchemy.orm import relationship


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)

    def find_all():
        
        try:
            return session.query(Product).all()
        except Exception as e:
            return e
        finally:
            session.close()







