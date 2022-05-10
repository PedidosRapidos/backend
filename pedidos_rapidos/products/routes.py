import logging

from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/")
def get_products(
        db: Session = Depends(database.get_db), q: str = None ):
    logger.info(q)
    try:
        products = crud.get_products(db, q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return [schemas.CreateProductResponse(**product.dict()) for product in products]
