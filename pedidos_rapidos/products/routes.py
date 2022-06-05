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
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    try:
        product_qualification = crud.get_product(db, product_id)
        return schemas.ProductResponse.from_qualified_product(product_qualification)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/{image_id}/")
def get_image(image_id: int, db: Session = Depends(database.get_db)):
    try:
        image = crud.get_image(db, image_id)
        return StreamingResponse(BytesIO(image.content), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}/image/")
def get_product_image(product_id: int, db: Session = Depends(database.get_db)):
    try:
        product = crud.get_product_image(db, product_id)
        image = product.image
        return StreamingResponse(BytesIO(image.content), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{product_id}")
async def put_product(
    product_id: int, request: Request, db: Session = Depends(database.get_db)
):
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
                data[key] = val

        if form.get("image") is not None:
            data["image"] = database.Image(content=await form["image"].read())

        product = crud.modify_product(db, product_id, data)
        return schemas.CreateProductResponse.from_product(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_products(
    db: Session = Depends(database.get_db),
    q: str = None,
    page: int | None = None,
    page_size: int | None = None,
    field: str = None,
    order: str = None,
):
    try:
        qualified_products = crud.get_products(
            db, query=q, page=page, page_size=page_size, field=field, order=order
        )
        return [
            schemas.ProductResponse.from_qualified_product(product_qualification)
            for product_qualification in qualified_products
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
