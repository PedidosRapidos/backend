from . import models, crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_db


router = APIRouter(prefix="/sellers")


@router.post(
    "/{seller_id}/shops/",
    response_model=schemas.CreateShopResponse)
def post_item(
        seller_id: int,
        create_shop_req: schemas.CreateShopRequest,
        db: Session = Depends(get_db)):
    try:
        shop = crud.create_shop(db,
                                seller_id,
                                models.Shop(**create_shop_req.dict()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateShopResponse(**shop.dict())
