import json
import logging

from sqlmodel import Session, select

from pedidos_rapidos.cart.crud import get_cart
from .schemas import CreateOrderRequest

from ..database import Order, Cart
from ..utils.enum_utils import OrderState

logger = logging.getLogger("uvicorn")


def create_order_from_cart(db:Session, cart_id: int, req: CreateOrderRequest):
    client = get_cart(db, cart_id).client
    order = Order(cart_id=cart_id, state=OrderState.TO_CONFIRM, payment_method=req.payment_method, client_id=client.id)

    new_cart = Cart(client_id=client.id)
    client.cart = new_cart
    db.add(order)
    
    db.commit()

    db.refresh(order)
    db.refresh(client)

    return order
