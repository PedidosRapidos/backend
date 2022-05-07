from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .. import database


router = APIRouter(prefix="/sellers")


@router.post(
    "/{seller_id}/shops/",
    response_model=schemas.CreateShopResponse)
def post_item(
        seller_id: int,
        create_shop_req: schemas.CreateShopRequest,
        db: Session = Depends(database.get_db)):
    try:
        shop = crud.create_shop(db,
                                seller_id,
                                database.Shop(**create_shop_req.dict()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateShopResponse(**shop.dict())

@router.post("/", response_model=schemas.CreateSellerResponse)
def post_seller(
        create_seller_req: schemas.CreateSellerRequest,
        db: Session = Depends(database.get_db)):
    try:
        seller = crud.create_seller(db,
                                    database.Seller(**create_seller_req.dict()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateSellerResponse(**seller.dict())   
