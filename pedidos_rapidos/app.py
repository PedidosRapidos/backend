from fastapi import FastAPI
from .sellers.routes import router as seller_router
from .products.routes import router as products_router
from .cart.routes import router as cart_router
from .user.routes import router as user_router

app = FastAPI()
app.include_router(seller_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(user_router)
