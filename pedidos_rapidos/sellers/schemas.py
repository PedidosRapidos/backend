import email
from pydantic import BaseModel


class CreateShopRequest(BaseModel):
    address: str
    cbu: str

class CreateShopResponse(BaseModel):
    id: int | None = None
    address: str
    cbu: str

class CreateSellerRequest(BaseModel):
    email: str
    password: str

class CreateSellerResponse(BaseModel):
    id: int | None = None
    email: str
    password: str
