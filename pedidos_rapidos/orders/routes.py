import logging
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import database

router = APIRouter(prefix="/orders")

logger = logging.getLogger("uvicorn")


@router.post("/{user_id}")
def post_order(
    user_id: int,
    create_order_request: schemas.CreateOrderRequest,
    db: Session = Depends(database.get_db),
) -> schemas.CreateOrderResponse:
    try:
        logger.info("creating order")
        order = crud.create_order_from_cart(db, user_id, create_order_request)
        return schemas.CreateOrderResponse.from_model(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{order_id}/product/{product_id}/review")
def review_order(
    order_id: int,
    product_id: int,
    review: schemas.ReviewOrderProductRequest,
    db: Session = Depends(database.get_db),
) -> schemas.CreateOrderResponse:
    try:
        logger.info("creating review from order")
        qualification = crud.review_order(db, order_id, product_id, review.qualification)
        print(qualification.dict())
        return schemas.ReviewOrderProductResponse(**review.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{order_id}/repeat")
def repeat_order(
    order_id: int,
    create_order_request: schemas.CreateOrderRequest,
    db: Session = Depends(database.get_db),
) -> schemas.CreateOrderResponse:
    try:
        logger.info("repeating order")
        order = crud.repeat_order(db, order_id, create_order_request)
        return schemas.CreateOrderResponse.from_model(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_orders(
    client_id: int,
    q: str | None = None,
    shop_id: int | None = None,
    state: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    order: str | None = None,
    order_by: str | None = None,
    db: Session = Depends(database.get_db),
) -> list[schemas.CreateOrderResponse]:
    try:
        logger.info("get order")
        orders = crud.get_orders(
            db,
            client_id,
            q=q,
            state=state,
            shop_id=shop_id,
            page=page,
            page_size=page_size,
            order=order,
            order_by=order_by,
        )
        return list(map(schemas.CreateOrderResponse.from_model, orders))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/")
def change_state(
    order_id: int,
    change_order_request: schemas.ChangeOrderStateRequest,
    db: Session = Depends(database.get_db),
) -> schemas.CreateOrderResponse:
    try:
        order = crud.change_state(db, order_id, change_order_request)
        return schemas.CreateOrderResponse.from_model(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))