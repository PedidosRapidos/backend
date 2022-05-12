import logging
from . import crud, schemas
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from .. import database


router = APIRouter(prefix="/shops")

logger = logging.getLogger("uvicorn")

LIST_LIMIT=10

@router.get("/")
def get_shops(
        db: Session = Depends(database.get_db), page: int = 1 ):
    try:
        offset = LIST_LIMIT * (page - 1)

        shops = crud.get_shops(db, offset, LIST_LIMIT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return [schemas.ShowShopResponse(**shop.dict()) for shop in shops]