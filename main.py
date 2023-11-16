from fastapi import FastAPI
from routers import product_router, category_router

from models import db

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


app.include_router(
    router=product_router,
    prefix='/api/v1/products'
)

app.include_router(
    router=category_router,
    prefix='/api/v1/categories'
)
