import json
import random
from sqlalchemy.orm import Session

from app.api.models.inventory import Inventory, Transaction
from ..models import Category, Product
from pathlib import Path


def initialize_default_products(db: Session, json_path: str = "./api/utils/default_inventory.json"):
    """Carga datos del inventario por defecto solo si las tablas están vacías."""
    
    # Verifica si hay datos en las tablas
    if db.query(Category).count() > 0 or db.query(Product).count() > 0:
        return
    
    json_file = Path(json_path)
    if not json_file.exists():
        print("Archivo JSON no encontrado.")
        return
    
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

 
    # Cargar categorías
    category_dict = {}
    for category_data in data.get("categories", []):
        category = Category(name=category_data["name"])
        db.add(category)
        db.commit()
        db.refresh(category)
        category_dict[category.name] = category.id

    # Cargar productos
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

    new_inventory_count = db.query(Inventory).count()
    new_transactions_count = db.query(Transaction).count()
    
    initialize_default_products(db)

    products = Product.find_all()
    inventories = Inventory.find_all()

    if len(inventories) > 0:
        return
    
    for product in products:
        # Verificar si el producto ya tiene inventario para evitar duplicados
        existing_inventory = db.query(Inventory).filter_by(product_id=product.id).first()
        if existing_inventory:
            continue  # Si ya existe, no lo agregamos nuevamente

        random_quantity = random.randint(42, 256)
        inventory = Inventory(product_id=product.id, quantity=random_quantity)
        db.add(inventory)  
        db.flush()

        transaction = Transaction(inventory_id=inventory.id, type="stockin", quantity=random_quantity)
        db.add(transaction)

    db.commit()  
