from ..database import Product
from sqlmodel import Session, select


def get_product(
        db: Session,
        product_id: int) -> Product:
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise Exception("Product no existe")
    return product

def get_products(
        db: Session,
        query: str = None) -> Product:
    product_query = select(Product)

    if query is not None:
        product_query = product_query.where(Product.name.ilike(query))

    return db.exec(product_query)
