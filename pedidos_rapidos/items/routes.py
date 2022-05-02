from . import models, crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_db
import logging
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/items")

logger = logging.getLogger("uvicorn")


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(
        item_id: int,
        db: Session = Depends(get_db)):
    logger.info("get_item %s", item_id)
    item = crud.read_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return schemas.Item(**item.dict())


@router.put("/{item_id}")
def put_item(
        item_id: int,
        item: schemas.Item,
        db: Session = Depends(get_db)):
    item.id = item_id
    try:
        updated = crud.update_item(
                db,
                models.Item(**item.dict()))
        return schemas.Item(**updated.dict())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Already exists")
