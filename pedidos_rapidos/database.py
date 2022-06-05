import os
from typing import List, Optional
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship
import sqlalchemy as sa

from pedidos_rapidos.utils.enum_utils import OrderState


class Seller(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    username: str
    token: str | None = None
    shops: List["Shop"] = Relationship(back_populates="seller")


class Client(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    username: str
    token: str | None
    orders: Optional[List["Order"]] = Relationship(back_populates="client")
    cart: Optional["Cart"] = Relationship(
        sa_relationship=RelationshipProperty("Cart", uselist=False)
    )


class Shop(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cbu: str
    address: str
    name: str
    seller_id: int = Field(default=None, foreign_key="seller.id")
    seller: Seller = Relationship(back_populates="shops")
    product: List["Product"] = Relationship(back_populates="shop")
    orders: Optional[List["Order"]] = Relationship(back_populates="shop")

class Image(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    content: bytes = Field(sa_column=sa.Column("image", sa.LargeBinary))

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    price: int = Field(default=None)
    name: str
    description: str
    image_id: int = Field(default=None, foreign_key="image.id")
    image: Image = Relationship()
    shop_id: int = Field(default=None, foreign_key="shop.id")
    shop: Shop = Relationship(back_populates="product")


class Order(SQLModel, table=True):
    __tablename__ = "order"
    id: int = Field(default=None, primary_key=True)
    cart_id: int = Field(default=None, foreign_key="cart.id")
    cart: "Cart" = Relationship()
    state: OrderState = Field(sa_column=sa.Column("state", sa.Enum(OrderState)))
    payment_method: str = Field(default=None)
    address: str = Field(default=None)
    client_id: int = Field(default=None, foreign_key="client.id")
    client: Client = Relationship()
    shop_id: int = Field(default=None, foreign_key="shop.id")
    shop: Shop = Relationship()


class ProductCart(SQLModel, table=True):
    __tablename__ = "product_cart"
    id: int = Field(default=None, primary_key=True)
    quantity: int
    product_id: int = Field(default=None, foreign_key="product.id")
    product: Product = Relationship()


class CartProductCartLink(SQLModel, table=True):
    product_cart_id: int = Field(
        default=None, foreign_key="product_cart.id", primary_key=True
    )
    cart_id: int = Field(default=None, foreign_key="cart.id", primary_key=True)


class Cart(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    products: List[ProductCart] = Relationship(link_model=CartProductCartLink)
    client_id: int = Field(default=None, foreign_key="client.id")
    client: Client = Relationship()


class Review(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    qualification: int = Field(default=None)
    product_id: int = Field(default=None, foreign_key="product.id")
    product: Product = Relationship()
    order_id: int = Field(default=None, foreign_key="order.id")
    order: Order = Relationship()


# Database will be initialize in main.py alembic/env.py but customized in tests.

engine = None
metadata = None


def databse_url():
    uri = os.getenv("DATABASE_URL", "")
    return uri.replace("postgres://", "postgresql://")


def init():
    global engine
    global metadata
    engine = create_engine(databse_url())
    metadata = SQLModel.metadata.create_all(engine)
    return metadata


def get_db() -> Session:
    with Session(engine) as session:
        yield session
