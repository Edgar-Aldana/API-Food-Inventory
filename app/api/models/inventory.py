from fastapi import logger
from ..connection import session, Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False, default=0)

    product = relationship("Product", back_populates="inventory")
    transactions = relationship("Transaction", back_populates="inventory")

    def find_all():
        try:
            return session.query(Inventory).all()
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    
    def find_by_filter(**args):
        try:
            return session.query(Inventory).filter_by(**args).first()
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()


    def create(product_id: int, quantity: int):
        try:
            new_inventory = Inventory(product_id=product_id, quantity=quantity)
            session.add(new_inventory)
            session.commit()
            session.refresh(new_inventory)
            return new_inventory
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    
    def update(inventory_id: int, quantity: int):
        try:
            inventory_db = session.query(Inventory).filter_by(id=inventory_id).first()
            inventory_db.quantity = quantity
            session.commit()
            session.refresh(inventory_db)
            return inventory_db
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()
    

    def delete(inventory_id: int):
        try:
            inventory = session.query(Inventory).filter_by(id=inventory_id).first()
            session.delete(inventory)
            session.commit()
            return inventory
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()
        


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    type = Column(String, nullable=False)  # "in" (stock in) or "out" (stock out)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="transactions")


    def find_all():
        try:
            return session.query(Transaction).all()
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close

    
    def find_by_filter(**args):
        try:
            return session.query(Transaction).filter_by(**args).first()
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close()

    
    def create(inventory_id: int, type: str, quantity: int):
        try:
            new_transaction = Transaction(inventory_id=inventory_id, type=type, quantity=quantity)
            session.add(new_transaction)
            session.commit()
            session.refresh(new_transaction)
            return new_transaction
        except Exception as e:
            logger.error(e)
            return None
        finally:
            session.close


    