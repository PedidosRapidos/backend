from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: int
    image: str


class CreateProductResponse(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: int


class ProductResponse(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: int
    qualification: float
