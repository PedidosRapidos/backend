from ..database import Shop, Product
from sqlmodel import Session, select, desc, asc, func

def get_shops(
        db: Session,
        offset: int,
        limit: int) -> Shop:

    return db.exec(select(Shop).limit(limit).offset(offset))


def get_products_from_shop(
        db: Session,
        shop_id: int,
        query: str = None,
        page:int = None,
        page_size :int = None,
        field: str = None,
        order: str = None) -> list[Product]:

    product_query = select(Product)

    if query is not None:
        product_query = product_query.where(Product.name.ilike(f"%{query}%"), Product.shop_id == shop_id)
    if page is not None and page_size is not None:
        product_query = product_query.where(Product.shop_id == shop_id).offset(page_size*page).limit(page_size)

    if field is not None:
        if order == 'desc':
            product_query = product_query.where(Product.shop_id == shop_id).order_by(desc(Product.price), asc(Product.id))
        else:
            product_query = product_query.where(Product.shop_id == shop_id).order_by(asc(Product.price), asc(Product.id))
    else:
        product_query = product_query.where(Product.shop_id == shop_id).order_by(asc(Product.id))

    return db.exec(product_query).all()
