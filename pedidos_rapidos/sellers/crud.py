from ..database import Shop, Seller, Product
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
    shop.seller_id = seller_id
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

def create_product(
        db: Session,
        seller_id: int,
        shop_id: int,
        product: Product) -> Product:
    existent_shop = db.exec(select(Shop).where(Shop.id == shop_id)).first()
    if existent_shop is None:
        raise Exception("Shop no existe")
    product.shop_id = shop_id
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_shops(
        db: Session,
        seller_id: int,
        offset: int,
        limit: int) -> Shop:

    return db.exec(select(Shop).where(Shop.seller_id == seller_id).limit(limit).offset(offset))
