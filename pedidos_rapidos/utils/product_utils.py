from sqlmodel import Session, select

from pedidos_rapidos.database import Product


def product_exist(db, product):
    prod = db.exec(select(Product).where(Product.id == product.id)).first()
    return prod is not None
