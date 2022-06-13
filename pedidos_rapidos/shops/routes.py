import logging
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .. import database

router = APIRouter(prefix="/shops")

logger = logging.getLogger("uvicorn")

LIST_LIMIT = 10


@router.get("/")
def get_shops(
        db: Session = Depends(database.get_db),
        page: int = 1,
        q: str = None):
    try:
        offset = LIST_LIMIT * (page - 1)
        shops = crud.get_filtered_shops(db, offset, LIST_LIMIT, q)
        return [schemas.ShowShopResponse(**shop.dict()) for shop in shops]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{shop_id}")
def get_shop(
        shop_id:int,
        db: Session = Depends(database.get_db),
):
    try:
        shop = crud.get_shop(db, shop_id)
        if shop is None:
            raise Exception("Shop not found")
        return schemas.ShowShopResponse(**shop.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/{shop_id}/products"
)
def get_products_in_shop(
        shop_id: int,
        db: Session = Depends(database.get_db),
        q: str = None,
        page: int | None = None,
        page_size: int | None = None,
        field: str = None,
        order: str = None
):
    try:
        products = crud.get_products_from_shop(db, shop_id,
                                               query=q,
                                               page=page,
                                               page_size=page_size,
                                               field=field,
                                               order=order)

        return schemas.ShopProductsResponse.from_model(products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
