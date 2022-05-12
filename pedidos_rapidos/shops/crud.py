from ..database import Shop
from sqlmodel import Session, select

def get_shops(
        db: Session,
        offset: int,
        limit: int) -> Shop:

    return db.exec(select(Shop).limit(limit).offset(offset))
