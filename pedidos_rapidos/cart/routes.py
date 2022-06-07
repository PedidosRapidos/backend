from typing import List

from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .. import database
import logging



router = APIRouter(prefix="/shopping_cart")

logger = logging.getLogger("uvicorn")


@router.post("/{cart_id}/products/",  response_model=schemas.CartResponse)
def post_in_cart(
        cart_id:int,
        add_request: schemas.CartProductRequest,
        db: Session = Depends(database.get_db)):
    cart = crud.add_to_cart(db, cart_id, add_request)
    if cart  is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return schemas.CartResponse.from_model(cart)


@router.delete("/{cart_id}/products/{product_id}",  response_model=schemas.CartResponse)
def remove_from_cart(
        cart_id: int,
        product_id: int,
        db: Session = Depends(database.get_db)):
    cart = crud.remove_from_cart(db, cart_id, product_id)
    if cart  is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.from_model(cart)


@router.get("/{cart_id}",  response_model=schemas.CartResponse)
def get_cart(
        cart_id: int,
        db: Session = Depends(database.get_db)):
    cart = crud.get_cart(db, cart_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return schemas.CartResponse.from_model(cart)


@router.put("/{cart_id}",  response_model=schemas.CartResponse)
def replace_cart(cart_id: int,
                 replace_request: schemas.ReplaceCartRequest,
                 db: Session = Depends(database.get_db)):
    try:
        cart = crud.replace_cart(db, cart_id, replace_request)
        return schemas.CartResponse.from_model(cart)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

