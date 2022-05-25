import json
import logging

from sqlmodel import Session, select

from pedidos_rapidos.products.crud import get_product
from pedidos_rapidos.users.crud import get_client

from .schemas import CartProductRequest, CreateCartRequest, CartProdResponse
from ..database import Cart, Product, ProductCart

logger = logging.getLogger("uvicorn")


def add_to_cart(db: Session, cart_id: int, add_request: CartProductRequest):
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")

    product = db.exec(select(Product).where(Product.id == add_request.product_id)).first()
    if product is None:
        raise Exception("Product does not exists.")

    db.refresh(cart)
    exist_prod = list(filter(lambda p: p.product_id == add_request.product_id, list(cart.products)))

    if len(exist_prod) != 0:
        exist_prod[0].quantity = add_request.quantity
    else:
        product = ProductCart(product_id=add_request.product_id, quantity=add_request.quantity)
        cart.products.append(product)

    db.commit()
    db.refresh(cart)
    return cart


def remove_from_cart(db: Session,
                     cart_id: int,
                     product_id: int):
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")

    db.refresh(cart)
    products = [product
                for product in cart.products
                if product.product_id != product_id]
    cart.products = products
    db.commit()
    db.refresh(cart)
    return cart


def get_cart(db: Session, cart_id: int) -> Cart:
    cart = db.exec(select(Cart).where(Cart.id == cart_id)).first()
    if cart is None:
        raise Exception("Cart does not exists.")
    db.refresh(cart)
    return cart


def get_products_from_cart(db: Session, cart_id: int):
    cart = get_cart(db, cart_id)

    cart_prod = [CartProdResponse(product=get_product(db, product_id=prod.product_id),
                                  quantity=prod.quantity) for prod in cart.products]

    return cart_prod


def clear_cart(db: Session,
               cart_id: int):
    cart = get_cart(db, cart_id=cart_id)
    cart.products = []
    db.commit()
    db.refresh(cart)
    return cart
