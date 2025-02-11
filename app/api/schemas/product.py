from typing import List, Optional
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


class ProductCreate(BaseModel):

    name: str
    description: str
    price: float
    category: str
    stock: int



class ProductUpdate(BaseModel):

    id: int
    name: str
    category: str
    description: str
    price: float
    stock: int
    




class Product(ProductBase):
    id: int
    category: Optional[str] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True


class ProductRequestData(BaseModel):

    product_id: int
    quantity: int


class ProductRequest(BaseModel):

    products: List[ProductRequestData]


######## schemas output API Responses ########


class GetAllProducts(BaseModel):
    products: list[Product]
    categories: list[str]

class APIResponseGetAllProducts(APIResponse):
    payload: GetAllProducts




######## schemas output API Responses ########

