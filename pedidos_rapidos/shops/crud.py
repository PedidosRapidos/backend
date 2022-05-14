from ..database import Shop
from sqlmodel import Session, select

def get_shops(
        db: Session,
        offset: int,
        limit: int) -> Shop:

    return db.exec(select(Shop).limit(limit).offset(offset))


def get_products_from_shop(
        db: Session,
        shop_id: int) -> Shop:
    shop = db.exec(select(Shop).where(Shop.id == shop_id)).first()
    if shop is None:
        raise Exception("Shop no existe")

    return shop.product