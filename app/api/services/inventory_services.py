
from app.api.models.inventory import Inventory, Transaction
from app.api.schemas.inventory import Inventory as InventorySchema


class InventoryService:
    def __init__(self):
        pass

    @staticmethod
    def find_all():
        
        inventories = [InventorySchema(**inventory.__dict__) for inventory in Inventory.find_all()]
        return inventories
    
    @staticmethod
    def find_by_filter(**args):

        inventory = Inventory.find_by_filter(**args)
        inventory = InventorySchema(**inventory.__dict__)
        return inventory


    @staticmethod
    def stockIn(inventory_id: int, quantity_to_add: int):

        stock_inventary = Inventory.find_by_filter(id=inventory_id)
        stock_inventary.quantity += quantity_to_add

        updated_inventory = Inventory.update(inventory_id, stock_inventary.quantity)
        return InventorySchema(**updated_inventory.__dict__)
    
    @staticmethod
    def stockOut(inventory_id: int, quantity_to_substract: int):

        stock_inventary = Inventory.find_by_filter(id=inventory_id)
        stock_inventary.quantity -= quantity_to_substract

        updated_inventory = Inventory.update(inventory_id, stock_inventary.quantity)

        TransactionService.register("stock_out", quantity_to_substract, inventory_id)
    
        return InventorySchema(**updated_inventory.__dict__)




class TransactionService():

    
    @staticmethod
    def register(type: str, quantity: int, inventory_id: int):
        Transaction.create(inventory_id, type, quantity)