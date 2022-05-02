from fastapi import FastAPI
from .database import *  # noqa: F401,F403
from .items.routes import router as item_router

app = FastAPI()
app.include_router(item_router)
