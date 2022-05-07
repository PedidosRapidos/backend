from ..database import Shop, Seller
from sqlmodel import Session, select


def create_shop(
        db: Session,
        seller_id: int,
        shop: Shop) -> Shop:
    # get shop
    seller = db.exec(select(Seller).where(Seller.id == seller_id)).first()
    if seller is None:
        raise Exception("Seller no existe")
    shop.seller = seller
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

def create_seller(
        db: Session,
        seller: Seller) -> Seller:
    existent_seller = db.exec(select(Seller).where(Seller.email == seller.email)).first()
    if existent_seller is not None:
        raise Exception("Seller ya existente con ese email")
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller
