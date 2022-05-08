from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import database


router = APIRouter(prefix="/products")

@router.get(
    "/{product_id}")
def get_product(
        product_id: int,
        db: Session = Depends(database.get_db)):
    try:
        product = crud.get_product(db,
                                product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateProductResponse(**product.dict())
