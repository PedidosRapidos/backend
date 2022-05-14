from typing import List

from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import database
import logging



router = APIRouter(prefix="/shopping_cart")

logger = logging.getLogger("uvicorn")


@router.post("/",  response_model=schemas.CartResponse)
def create_cart(
        cart_request: schemas.CreateCartRequest,
        db: Session = Depends(database.get_db)):
    logger.info("saving products cart")
    cart = crud.create_cart(db, cart_request.client_id, cart_request.products)

    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.fromModel(cart)


@router.post("/{cart_id}/products/",  response_model=schemas.CartResponse)
def post_in_cart(
        cart_id:int,
        add_request:schemas.CartProductRequest,
        db: Session = Depends(database.get_db)):
    cart = crud.add_to_cart(db, cart_id, add_request)

    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.fromModel(cart)

@router.delete("/{cart_id}/products",  response_model=schemas.CartResponse)
def remove_from_cart(
        cart_id:int,
        remove_request: schemas.CartProductRequest,
        db: Session = Depends(database.get_db)):
    cart = crud.remove_from_cart(db, cart_id, remove_request)

    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.fromModel(cart)

@router.get("/{cart_id}",  response_model=schemas.CartResponse)
def get_cart(
        cart_id: int,
        db: Session = Depends(database.get_db)):
    cart = crud.get_cart(db, cart_id)

    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.fromModel(cart)
