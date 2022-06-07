from pydantic import BaseModel

from pedidos_rapidos.database import Product
from pedidos_rapidos.products.schemas import CreateProductResponse


class CartProductRequest(BaseModel):
    product_id: int
    quantity: int


class CartProductResponse(CreateProductResponse):
    quantity: int


class CartRequest(BaseModel):
    client_id: int
    products: list[dict] = []


class CreateCartRequest(BaseModel):
    client_id: int
    products: list[CartProductRequest] = []

    @staticmethod
    def from_model(cart_request):
        products = [CartProductRequest(**p) for p in cart_request.products]
        return CreateCartRequest(client_id=cart_request.client_id,
                                 products=products)



class CartProdResponse(BaseModel):
    product: Product | None = None
    quantity: int | None = None



class CartResponse(BaseModel):
    id: int | None = None
    products: list[CartProductResponse] | None = None

    @staticmethod
    def from_model(cart):

        products = [CartProductResponse(**(CreateProductResponse.from_product(cart_prod.product).dict()),
                                        quantity=cart_prod.quantity) for cart_prod in cart.products]
        return CartResponse(id=cart.id,
                            products=products)


class ReplaceCartRequest(BaseModel):
    cart_id: int