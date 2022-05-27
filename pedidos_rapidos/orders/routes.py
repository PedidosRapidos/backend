import logging
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .. import database

router = APIRouter(prefix="/orders")

logger = logging.getLogger("uvicorn")


@router.post(
    "/{cart_id}"
)
def post_order(
        cart_id: int, create_order_request: schemas.CreateOrderRequest,
        db: Session = Depends(database.get_db),
):
    try:
        logger.info("creating order")
        order = crud.create_order_from_cart(db, cart_id, create_order_request)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return schemas.CreateOrderResponse.from_model(order)
