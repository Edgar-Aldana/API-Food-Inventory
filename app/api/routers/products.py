from fastapi import APIRouter
from app.api.services.product_services import ProductService
from app.api.schemas.product import APIResponseGetAllProducts, GetAllProducts, ProductCreate, ProductBase

products_router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)

product_services = ProductService()

@products_router.get("/", response_model=APIResponseGetAllProducts)
async def get_products():

    response = ProductService.find_all()
    response = GetAllProducts(products=response)
    response = APIResponseGetAllProducts(success=True, message="Products Found", payload=response).dict()
    return response

@products_router.get("/{product_id}")
async def get_product(product_id: int):
    return ProductService.find_by_filter(id=product_id)


