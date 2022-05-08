from fastapi import FastAPI
from .items.routes import router as item_router
from .sellers.routes import router as seller_router

app = FastAPI()
app.include_router(item_router)
app.include_router(seller_router)