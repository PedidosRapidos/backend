from typing import List

from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import database
import logging



router = APIRouter(prefix="/shopping_cart")

logger = logging.getLogger("uvicorn")


@router.post("/",  response_model=schemas.CartResponse)
def add_products_to_cart(
        cart_request: schemas.CartRequest,
        db: Session = Depends(database.get_db)):
    logger.info("saving products cart")
    cart = crud.create_cart(db, cart_request)

    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return cart


