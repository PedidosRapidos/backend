import json
import logging

from sqlmodel import Session, select

from pedidos_rapidos.cart.crud import get_products_from_cart, get_cart, clear_cart
from pedidos_rapidos.products.crud import get_product

from ..database import Order, ProductOrder

logger = logging.getLogger("uvicorn")


def create_order_from_cart(db:Session, cart_id: int):
    cart = get_cart(db, cart_id=cart_id)
    products = get_products_from_cart(db, cart_id=cart_id)

    order = Order(user_id=cart.client_id)
    order.products = []

    for product in products:
        originalProduct = get_product(db, product_id=product.product.id)
        product = ProductOrder(product_id=product.product.id, quantity=product.quantity, price=originalProduct.price)
        order.products.append(product)

    print(order)
    clear_cart(db, cart_id=cart_id)
    print('hi')
    
    db.commit()
    print('commited')

    db.refresh(order)
    print(order)

    return order
