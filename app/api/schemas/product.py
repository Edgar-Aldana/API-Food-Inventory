from pydantic import BaseModel, Field

from app.api.schemas.globals.responses import APIResponse

class ProductBase(BaseModel):

    name: str
    description: str
    price: float
    category_id: int


class ProductBaseOutput(BaseModel):
    name: str = Field(alias="nombre")
    description: str = Field(alias="descripcion")
    price: float = Field(alias="precio")
    category_id: str = Field(alias="categoria_id")


class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True



######## schemas output API Responses ########


class GetAllProducts(BaseModel):
    products: list[Product]

class APIResponseGetAllProducts(APIResponse):
    payload: GetAllProducts




######## schemas output API Responses ########

