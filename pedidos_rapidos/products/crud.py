from ..database import Product, Review
from sqlmodel import Session, select, desc, asc, func


def get_product(db: Session, product_id: int):
    product = db.exec(
        select(Product, func.avg(Review.qualification).label("average"))
        .group_by(Product.id)
        .where(Product.id == product_id)
        .join(Review, Review.product_id == Product.id, isouter=True)
    ).first()
    if product is None:
        raise Exception("Product no existe")
    return product


def get_product_image(db: Session, product_id: int) -> Product:
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise Exception("Product no existe")
    return product


def modify_product(db: Session, product_id: int, product_data: dict) -> Product:

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
    page: int = None,
    page_size: int = None,
    field: str = None,
    order: str = None,
) -> list:
    average = func.avg(Review.qualification).label("average")
    product_query = (
        select(Product, average)
        .join(Review, Review.product_id == Product.id, isouter=True)
        .group_by(Product.id)
    )

    if query is not None:
        product_query = product_query.where(Product.name.ilike(f"%{query}%"))
    if page is not None and page_size is not None:
        product_query = product_query.offset(page_size * page).limit(page_size)

    if field is not None:
        if order == "desc":
            product_query = product_query.order_by(desc(Product.price), asc(Product.id))
        else:
            product_query = product_query.order_by(asc(Product.price), asc(Product.id))
    else:
        product_query = product_query.order_by(asc(Product.id))

    return db.exec(product_query).all()
