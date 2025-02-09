import json
from sqlalchemy.orm import Session
from ..models import Category, Product
from pathlib import Path

def initialize_default_inventory(db: Session, json_path: str = "./api/utils/default_inventory.json"):
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
    print("✅ Inventario por defecto cargado con éxito.")
