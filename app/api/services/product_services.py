from app.api.models.categories import Category
from app.api.models.inventory import Inventory
from ..schemas.product import ProductCreate, ProductBase, Product as ProductDB
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
        new_product = Product.create(product)
        return ProductBase(**new_product.__dict__)
    
    @staticmethod
    def update(product: ProductBase):
        updated_product = Product.update(product.id, product)
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
