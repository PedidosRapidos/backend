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
        cart_id: int,
        db: Session = Depends(database.get_db),
):
    try:
        print(1)
        order = crud.create_order_from_cart(db, cart_id)
        print(2)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return schemas.OrderResponse.from_model(order)
