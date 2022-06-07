from pydantic import BaseModel


from pedidos_rapidos.products.schemas import ProductResponse


class ShowShopRequest(BaseModel):
    name: str
    address: str
    cbu: str

class ShowShopResponse(BaseModel):
    id: int | None = None
    name: str
    address: str
    cbu: str

class ShopProductsResponse(BaseModel):
    products: list[ProductResponse] | None = None

    @staticmethod
    def from_model(products):
        products = [ProductResponse.from_qualified_product(p) for p in products]
        return ShopProductsResponse(products=products)
