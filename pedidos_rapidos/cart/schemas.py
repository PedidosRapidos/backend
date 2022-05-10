import uuid
from typing import List

from pydantic import BaseModel

from pedidos_rapidos.database import Product


class CartRequest(BaseModel):
    products: List[Product] | None = None


class CartResponse(BaseModel):
    id: int | None = None
    products: List[Product] | None = None

