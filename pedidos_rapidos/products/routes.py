import logging

from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from io import BytesIO
from sqlmodel import Session
from .. import database


router = APIRouter(prefix="/products")

logger = logging.getLogger("uvicorn")

@router.get("/{product_id}")
def get_product(
        product_id: int,
        db: Session = Depends(database.get_db)):
    try:
        product = crud.get_product(db,
                                   product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateProductResponse(**product.dict())


@router.get("/{product_id}/image")
def get_product_image(
        product_id: int,
        db: Session = Depends(database.get_db)):
    try:
        product = crud.get_product(db,
                                   product_id)
        return StreamingResponse(BytesIO(product.image),
                                 media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/{product_id}")
async def put_product(
        product_id: int,
        request: Request,
        db: Session = Depends(database.get_db)):
    try:
        form = await request.form()
        logger.info(form)
        data = {}
        for key in ["price"]:
            val = form.get(key)
            if val is not None:
                data[key] = int(val)

        for key in ["name", "description"]:
            val = form.get(key)
            if val is not None:
                data[key] =val

        if form.get("image") is not None:
            data["image"] = await form["image"].read()

        product = crud.modify_product(db,
                                product_id,
                                data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateProductResponse(**product.dict())


@router.get("/")
def get_products(
        db: Session = Depends(database.get_db),
        q: str = None,
        order_by_price: str = None,
        order_by_name: str = None,
        page: int | None = None,
        page_size: int | None = None):
    try:
        products = crud.get_products(db,
                                     query=q,
                                     order_by_price=order_by_price,
                                     order_by_name=order_by_name,
                                     page=page,
                                     page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return [schemas.CreateProductResponse(**product.dict()) for product in products]
