from app.api.models.categories import Category
from app.api.models.inventory import Inventory
from app.api.services.inventory_services import TransactionService
from ..schemas.product import ProductCreate, ProductBase, Product as ProductDB, ProductUpdate
from ..models import Product
from app.api.schemas.category import Category as CategorySchema

class ProductService:

    def __init__(self):
        pass

    @staticmethod
    def find_all():

        products = [ProductDB(**product.__dict__) for product in Product.find_all()]

        for product in products:
            
            category = Category.find_by_filter(id=product.category_id)
            product.category = category.name

            inventory = Inventory.find_by_filter(id=product.id)
            product.stock = inventory.quantity

        return products


    def find_by_filter(**kwargs):
        product = Product.find_by_filter(**kwargs)
        return ProductBase(**product.__dict__)


    @staticmethod
    def create(product: ProductCreate):

        category_id = Category.find_by_filter(name=product.category).id
        quantity = product.stock
        product = product.dict()
        product.pop("stock")
        product.pop("category")

        new_product = Product.create(**{**product, "category_id": category_id})
        new_inventory = Inventory.create(product_id=new_product.id, quantity=quantity)

        TransactionService.register("stock_in", quantity, new_inventory.id)

        return ProductBase(**new_product.__dict__)
    
    @staticmethod
    def update(product_id, product: ProductUpdate):

        product_data = ProductCreate(**product.dict())

        updated_product = Product.update(product_id, product_data)
        updated_inventory = Inventory.update(updated_product.id, product.stock)
        
        if product.stock > updated_inventory.quantity:
            TransactionService.register("stock_in", product.stock - updated_inventory.quantity, updated_inventory.id)
        elif product.stock < updated_inventory.quantity:
            TransactionService.register("stock_out", updated_inventory.quantity - product.stock, updated_inventory.id)

        return ProductBase(**updated_product.__dict__)
    

    @staticmethod
    def delete(product_id: int):
        deleted_product = Product.delete(product_id)
        return ProductBase(**deleted_product.__dict__)


    @staticmethod
    def get_catalog():
        categories = Category.find_all()
        categories = [category.name for category in categories]
        return categories
