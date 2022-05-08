from ..database import Product
from sqlmodel import Session, select


def get_product(
        db: Session,
        product_id: int) -> Product:
    product = db.exec(select(Product).where(Product.id == product_id)).first()
    if product is None:
        raise Exception("Product no existe")
    return product
