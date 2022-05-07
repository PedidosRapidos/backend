from typing import List
from sqlmodel import Field, SQLModel, Relationship


class Seller(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    shops: List["Shop"] = Relationship()

class Shop(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cbu: str
    address: str
    seller_id: int = Field(default=None, foreign_key="seller.id")
    seller: Seller = Relationship(back_populates="seller")
