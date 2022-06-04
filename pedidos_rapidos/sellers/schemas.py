import email
from pydantic import BaseModel


class CreateShopRequest(BaseModel):
    name: str
    address: str
    cbu: str

class CreateShopResponse(BaseModel):
    id: int | None = None
    name: str
    address: str
    cbu: str

class CreateSellerRequest(BaseModel):
    email: str
    password: str
    username:str


class CreateSellerResponse(BaseModel):
    id: int | None = None
    email: str
    password: str

class CreateProductRequest(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: int
    image: str

class ShowShopResponse(BaseModel):
    id: int | None = None
    name: str
    address: str
    cbu: str
