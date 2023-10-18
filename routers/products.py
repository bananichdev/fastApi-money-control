from fastapi import APIRouter
from models import db, Product

router = APIRouter()


@router.get('/get')
async def get_products(read_all: bool = None):
    if read_all:
        query = Product.__table__.select()
        return await db.fetch_all(query=query)


@router.post('/add')
async def add_product(name: str, price: float, category_name: str):
    pass
