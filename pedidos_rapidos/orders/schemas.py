from __future__ import annotations

from enum import Enum

from pydantic import BaseModel

from pedidos_rapidos.database import Product
from pedidos_rapidos.cart.schemas import CartResponse
from pedidos_rapidos.utils.enum_utils import OrderState


class ReviewOrderProductRequest(BaseModel):
    qualification: int

class ReviewOrderProductResponse(BaseModel):
    qualification: int

class CreateOrderRequest(BaseModel):
    payment_method: str | None = None
    address: str | None = None

class CreateOrderResponse(BaseModel):
    id: int | None = None
    payment_method: str | None = None
    address: str | None = None
    state: OrderState | None = None
    cart: CartResponse | None = None

    @staticmethod
    def from_model(order):
        return CreateOrderResponse(
            id=order.id,
            payment_method=order.payment_method,
            address=order.address,
            state=order.state,
            cart=CartResponse.from_model(order.cart)
        )


class ChangeOrderStateRequest(BaseModel):
    new_state: OrderState | None = None
    client_id: int | None
    seller_id: int | None
