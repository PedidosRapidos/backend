import email
from typing import List

from pydantic import BaseModel

from pedidos_rapidos.database import Product
from pedidos_rapidos.products.schemas import CreateProductResponse


class ShowShopRequest(BaseModel):
    name: str
    address: str
    cbu: str

class ShowShopResponse(BaseModel):
    id: int | None = None
    name: str
    address: str
    cbu: str


class ShopProductsResponse(BaseModel):
    products: list[CreateProductResponse] | None = None

    @staticmethod
    def from_model(products):
        products = [CreateProductResponse(**p.dict()) for p in products]
        return ShopProductsResponse(products=products)
