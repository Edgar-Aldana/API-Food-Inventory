from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey

from app.api.models.categories import Category
from app.api.schemas.product import ProductCreate, ProductUpdate
from ..connection import session, Base
from sqlalchemy.orm import relationship


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True) 

    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)

    def find_all(isTrue: bool = True):
        
        try:
            return session.query(Product).filter_by(is_active=isTrue).all()
        except Exception as e:
            return e
        finally:
            session.close()

    

    def find_by_filter(**kwargs):
        try:
            return session.query(Product).filter_by(**kwargs).first()
        except Exception as e:
            return e
        finally:
            session.close()

    
    def create(**product):
        try:
            new_product = Product(**product)
            session.add(new_product)
            session.commit()
            session.refresh(new_product)
            return new_product
        except Exception as e:
            return e
        finally:
            session.close()
    

    def update(product_id: int, product: ProductCreate):
        try:
            product_db = session.query(Product).filter_by(id=product_id).first()
            product_db.name = product.name
            product_db.description = product.description
            product_db.price = product.price

            category_db = session.query(Category).filter_by(name=product.category).first()
            product_db.category_id = category_db.id
            session.commit()
            session.refresh(product_db)
            return product_db
        
        except Exception as e:
            return e
        finally:
            session.close()

    
    def delete(product_id: int):
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            session.delete(product)
            session.commit()
            return product
        except Exception as e:
            return e
        finally:
            session.close()


    def disable(product_id: int):
        try:
            product_db = session.query(Product).filter_by(id=product_id).first()
            product_db.is_active = False
            session.commit()
            session.refresh(product_db)
            return product_db
        except Exception as e:
            return e
        finally:
            session.close()





