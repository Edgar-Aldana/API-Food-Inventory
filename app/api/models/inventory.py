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



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    type = Column(String, nullable=False)  # "in" (stock in) or "out" (stock out)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="transactions")