from fastapi import APIRouter, HTTPException
from app.api.schemas.globals.responses import APIResponse
from app.api.services.product_services import ProductService
from app.api.schemas.product import APIResponseGetAllProducts, GetAllProducts, ProductCreate, ProductBase, ProductRequest, ProductUpdate
from app.api.services.inventory_services import InventoryService

products_router = APIRouter(
    prefix="/products",
    tags=["Products"],
    responses={404: {"description": "Not found"}},
)

product_services = ProductService()

@products_router.get("/", response_model=APIResponseGetAllProducts)
async def get_products():

    response = ProductService.find_all()
    catalog = ProductService.get_catalog()
    response = GetAllProducts(products=response, categories=catalog)
    response = APIResponseGetAllProducts(success=True, message="Products Found", payload=response).dict()
    return response

@products_router.get("/{product_id}")
async def get_product(product_id: int):
    return ProductService.find_by_filter(id=product_id)


@products_router.post("/", response_model=APIResponse)
async def create_product(product: ProductCreate):

    response = ProductService.create(product)
    return APIResponse(success=True, message="Product Created", payload=response.dict()).dict()


@products_router.put("/", response_model=APIResponse)
async def update_product(product: ProductUpdate):

    response = ProductService.update(product)
    return APIResponse(success=True, message="Product Updated", payload=response.dict()).dict()


@products_router.post("/request")
async def request_products(request: ProductRequest):
    try:
        
        for product in request.products:
         
            product_in_db = InventoryService.find_by_filter(id=product.product_id)
            if product_in_db and product_in_db.quantity >= product.quantity:
                InventoryService.stockOut(product.product_id, product.quantity)
            else:
                return APIResponse(success=False, message="Product not available", payload=None)
        
        return APIResponse(success=True, message="Products Requested", payload=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




