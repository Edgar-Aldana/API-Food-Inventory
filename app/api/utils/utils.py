import json
import random
from sqlalchemy.orm import Session

from app.api.models.inventory import Inventory, Transaction
from ..models import Category, Product
from ..models import User
from pathlib import Path
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def create_test_user(db: Session):
    
    existing_user = db.query(User).filter(User.username == "admin").first()
    
    if not existing_user:
        test_user = User(
            username="admin",
            password_hash=hash_password("admin123")  # Cambia la contraseña si lo deseas
        )
        db.add(test_user)
        db.commit()
    else:
        return None
    
    db.close()

def initialize_default_products(db: Session, json_path: str = "./api/utils/default_inventory.json"):
    """Carga datos del inventario por defecto solo si las tablas están vacías."""
    
    if db.query(Category).count() > 0 or db.query(Product).count() > 0:
        return
    
    json_file = Path(json_path)
    if not json_file.exists():
        print("Archivo JSON no encontrado.")
        return
    
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

 
    category_dict = {}
    for category_data in data.get("categories", []):
        category = Category(name=category_data["name"])
        db.add(category)
        db.commit()
        db.refresh(category)
        category_dict[category.name] = category.id

    
    for product_data in data.get("products", []):

        category_id = category_dict.get(product_data["category"])

        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            category_id=category_id,
        )
        db.add(product)

    db.commit()



def initialize_default_inventory(db: Session):
    
    initialize_default_products(db)
    create_test_user(db)

    products = Product.find_all()
    inventories = Inventory.find_all()

    if len(inventories) > 0:
        return
    
    for product in products:
        
        existing_inventory = db.query(Inventory).filter_by(product_id=product.id).first()
        if existing_inventory:
            continue  

        random_quantity = random.randint(42, 256)
        inventory = Inventory(product_id=product.id, quantity=random_quantity)
        db.add(inventory)  
        db.flush()

        transaction = Transaction(inventory_id=inventory.id, type="stockin", quantity=random_quantity)
        db.add(transaction)

    db.commit()  
