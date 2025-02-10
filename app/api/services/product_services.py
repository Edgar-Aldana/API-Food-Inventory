from ..schemas.product import ProductCreate, ProductBase, Product as ProductDB
from ..models import Product


class ProductService:

    def __init__(self):
        pass

    @staticmethod
    def find_all():

        products = [ProductDB(**product.__dict__) for product in Product.find_all()]
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

