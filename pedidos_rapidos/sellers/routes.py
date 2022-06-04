import logging
from pedidos_rapidos.products.schemas import CreateProductResponse
from pedidos_rapidos.orders.schemas import CreateOrderResponse
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .. import database


router = APIRouter(prefix="/sellers")

logger = logging.getLogger("uvicorn")

LIST_LIMIT = 10


@router.post("/{seller_id}/shops/", response_model=schemas.CreateShopResponse)
def post_shop(
    seller_id: int,
    create_shop_req: schemas.CreateShopRequest,
    db: Session = Depends(database.get_db),
):
    try:
        shop = crud.create_shop(db, seller_id, database.Shop(**create_shop_req.dict()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return schemas.CreateShopResponse(**shop.dict())


@router.post("/{seller_id}/shops/{shop_id}/products")
async def post_product(
    seller_id: int,
    shop_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    try:
        form = await request.form()
        logger.info(form)
        image = database.Image(content=await form["image"].read())
        data = {
            "id": None,
            "price": int(form["price"]),
            "name": form["name"],
            "description": form["description"],
            "image": image,
            "shop_id": shop_id,
        }

        product = crud.create_product(db, shop_id, database.Product(**data))
        return CreateProductResponse.from_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=schemas.CreateSellerResponse)
def post_seller(
    create_seller_req: schemas.CreateSellerRequest,
    db: Session = Depends(database.get_db),
):
    try:
        seller = crud.create_seller(db, database.Seller(**create_seller_req.dict()))
        return schemas.CreateSellerResponse(**seller.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{seller_id}/shops/")
def get_shops(
    seller_id: int,
    db: Session = Depends(database.get_db),
    page: int | None = None,
    page_size: int | None = None,
):
    try:
        shops = crud.get_shops(db, seller_id, page, page_size)
        return [schemas.ShowShopResponse(**shop.dict()) for shop in shops]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{seller_id}/shops/{shop_id}/orders/")
def get_orders(
    seller_id: int,
    shop_id: int,
    db: Session = Depends(database.get_db),
    page: int | None = None,
    page_size: int | None = None,
):
    try:
        orders = crud.get_orders(db, seller_id, shop_id, page, page_size)
        return [CreateOrderResponse.from_model(order) for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
