from pydantic import BaseModel

class InventoryBase(BaseModel):
    product_id: int
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int

    class Config:
        orm_mode = True





class TransactionBase(BaseModel):
    type: str
    quantity: int
    product_id: int
    inventory_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
