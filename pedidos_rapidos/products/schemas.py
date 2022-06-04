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
    qualification: float | None = None
    image_url: str| None = None

    @staticmethod
    def from_product(product):
        image_url = f"/products/images/{product.image_id}" if product.image_id else None
        extra = {"qualification": None,
                 "image_url": image_url }
        return CreateProductResponse(**(product.dict() | extra))


class ProductResponse(BaseModel):
    id: int | None = None
    name: str
    description: str
    price: int
    qualification: float | None = None
    image_url: str | None = None

    @staticmethod
    def from_qualified_product(product_qualification):
        (product, qualification) = product_qualification
        image_url = f"/products/images/{product.image_id}" if product.image_id else None
        extra = {"qualification": qualification,
                 "image_url": image_url }
        return ProductResponse(**(product.dict() | extra))
