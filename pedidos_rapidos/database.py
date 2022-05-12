from ctypes.wintypes import BYTE
import os
from typing import List
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship
import sqlalchemy as sa


class Seller(SQLModel, table=True):
     id: int = Field(default=None, primary_key=True)
     email: str
     password: str
     username: str
     shops: List["Shop"] = Relationship(back_populates="seller")

class Client(SQLModel, table=True):
     id: int = Field(default=None, primary_key=True)
     email: str
     password: str
     username: str

class Shop(SQLModel, table=True):
     id: int = Field(default=None, primary_key=True)
     cbu: str
     address: str
     seller_id: int = Field(default=None, foreign_key="seller.id")
     seller: Seller = Relationship(back_populates="shop")
     product: List["Product"] = Relationship(back_populates="shop")


class CartProductLink(SQLModel, table=True):
    product_id: int = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    cart_id: int = Field(
        default=None, foreign_key="cart.id", primary_key=True
    )


class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    price: int = Field(default=None)
    name: str
    description: str
    image: bytes = Field(sa_column=sa.Column("image",sa.LargeBinary))
    shop_id: int = Field(default=None, foreign_key="shop.id")
    shop: Shop = Relationship(back_populates="product")
    carts: List["Cart"] = Relationship(back_populates="products", link_model=CartProductLink)


class Cart(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="carts", link_model=CartProductLink)


# Database will be initialize in main.py alembic/env.py but customized in tests.

engine = None
metadata = None

def databse_url():
    uri = os.getenv("DATABASE_URL", "")
    return uri.replace("postgres://","postgresql://")
    
def init():
    global engine
    global metadata
    engine = create_engine(databse_url())
    metadata = SQLModel.metadata.create_all(engine)
    return metadata

def get_db() -> Session:
    with Session(engine) as session:
        yield session
