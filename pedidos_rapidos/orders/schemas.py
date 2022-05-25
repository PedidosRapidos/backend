from __future__ import annotations

from pydantic import BaseModel

from pedidos_rapidos.sellers.schemas import CreateProductResponse


class OrderProductResponse(CreateProductResponse):
    quantity: int
    price: int


class OrderResponse(BaseModel):
    id: int | None = None
    products: list[OrderProductResponse] | None = None

    @staticmethod
    def from_model(order):
        products = [OrderProductResponse(**order_prod.product.dict(),
                                         quantity=order_prod.quantity,
                                         price=order_prod.price) for order_prod in order.products]
        return OrderResponse(id=order.client_id,
                             products=products)
