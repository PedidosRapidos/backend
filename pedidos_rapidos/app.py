from fastapi import FastAPI
from .sellers.routes import router as seller_router
from .products.routes import router as products_router
from .cart.routes import router as cart_router
from .users.routes import router as users_router
from .shops.routes import router as shops_router
from .orders.routes import router as orders_router

app = FastAPI()
app.include_router(seller_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(users_router)
app.include_router(shops_router)
app.include_router(orders_router)
