import json
import logging


from sqlmodel import Session, select

from pedidos_rapidos.products.crud import get_product


from .schemas import CartProductRequest
from ..database import  Cart, Product

logger = logging.getLogger("uvicorn")


def create_cart(db: Session,
                product_ids: list[int]) -> Cart:
    products = [get_product(db, product_id) for product_id in product_ids]
    cart = Cart(products=products)
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart

def add_to_cart(db:Session, cart_id:int, add_request:CartProductRequest):
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")

    product = db.exec(select(Product).where(Product.id == add_request.product_id)).first()
    if product is None:
        raise Exception("Product does not exists.")

    db.refresh(cart)
    if any(p.id == add_request.product_id
           for p in list(cart.products)):
        # raise Exception("Product already in cart.")
        return cart

    cart.products.append(product)
    db.commit()
    db.refresh(cart)
    return cart

def remove_from_cart(db:Session,cart_id:int,rem_request:CartProductRequest):
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")

    db.refresh(cart)
    products = [product
                for product in cart.products
                    if product.id != rem_request.product_id]
    cart.products = products
    db.commit()
    db.refresh(cart)
    return cart

def get_cart(db:Session, cart_id:int):
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")
    db.refresh(cart)
    return cart
