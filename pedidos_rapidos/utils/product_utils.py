from sqlmodel import Session, select

from pedidos_rapidos.database import Product


def get_product(db:Session,
                product_id: int):
    prod = db.exec(select(Product).where(Product.id == product_id)).first()
    return prod
