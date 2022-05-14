from pydantic import BaseModel

from pedidos_rapidos.sellers.schemas import CreateProductResponse


class CreateCartRequest(BaseModel):
    client_id: int
    products: list[int] = []


class CartResponse(BaseModel):
    id: int | None = None
    products: list[CreateProductResponse] | None = None

    @staticmethod
    def fromModel(cart):
        products = [CreateProductResponse(**p.dict()) for p in cart.products]
        return CartResponse(id=cart.id,
                            products=products)

class CartProductRequest(BaseModel):
    product_id: int
