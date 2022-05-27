import json
import logging

from sqlmodel import Session, select

from pedidos_rapidos.cart.crud import get_products_from_cart, get_cart, clear_cart
from pedidos_rapidos.products.crud import get_product
from .schemas import CreateOrderRequest

from ..database import Order, Cart
from ..utils.order_state import OrderState

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
