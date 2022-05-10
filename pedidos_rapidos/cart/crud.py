import logging


from sqlmodel import Session, select


from .schemas import CartResponse, CartRequest
from ..database import  Cart
from .. import database
from ..utils.product_utils import product_exist

logger = logging.getLogger("uvicorn")


def create_cart(db: Session,
                cart_request: CartRequest) -> Cart:

    for product in cart_request.products:
        if not product_exist(db, product):
            raise Exception("No existe el producto")

    cart_validated = database.Cart(**cart_request.dict())
    db.add(cart_validated)
    db.commit()
    db.refresh(cart_validated)
    cart = CartResponse(**cart_request.dict())
    cart.id = cart_validated.id
    return cart
