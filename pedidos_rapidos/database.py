import os
from typing import List
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship


class Seller(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    shops: List["Shop"] = Relationship(back_populates="seller")

class Shop(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    cbu: str
    address: str
    seller_id: int = Field(default=None, foreign_key="seller.id")
    seller: Seller = Relationship(back_populates="shop")

# Database will be initialize in main.py alembic/env.py and customized in tests.

engine = None
metadata = None

def init():
    global engine
    global metadata
    engine = create_engine(os.getenv("DATABASE_URL", ""))
    metadata = SQLModel.metadata.create_all(engine)
    return metadata

def get_db() -> Session:
    with Session(engine) as session:
        yield session
