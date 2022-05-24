from ..database import Product
from sqlmodel import Session, select, desc, asc


def get_product(
        db: Session,
        product_id: int) -> Product:
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise Exception("Product no existe")
    return product

def modify_product(
        db: Session,
        product_id: int,
        product_data: dict) -> Product:
        
    existed_product = db.exec(select(Product).where(Product.id == product_id)).first()
    if existed_product is None:
        raise Exception("Product no existe")

    for key, value in product_data.items():
        setattr(existed_product, key, value)

    db.commit()
    db.refresh(existed_product)
    return existed_product

def get_products(
        db: Session,
        query: str = None,
        page:int = None,
        page_size :int = None,
        field: str = None,
        order: str = None) -> list[Product]:
    product_query = select(Product)

    if query is not None:
        product_query = product_query.where(Product.name.ilike(f"%{query}%"))
    if page is not None and  page_size is not None:
        product_query = product_query.offset(page_size*page).limit(page_size)

    if field is not None:
        if order == 'desc':
            product_query = product_query.order_by(desc(Product.price), asc(Product.id))
        else:
            product_query = product_query.order_by(asc(Product.price), asc(Product.id))
    else:
        product_query = product_query.order_by(asc(Product.id))

    return db.exec(product_query).all()
