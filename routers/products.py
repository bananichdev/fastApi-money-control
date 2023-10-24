from fastapi import APIRouter, Response, HTTPException, status

from models import ProductSchema
from controllers import read_products, read_category, write_product, read_product, purge_product

from datetime import date

router = APIRouter()


@router.get('/get', response_model=list[ProductSchema])
async def get_products(read_all: bool, sorting_by_price: bool = None,
                       select_by_date: date = None, select_by_category: str = None):
    try:
        return await read_products(read_all=read_all, sorting_by_price=sorting_by_price,
                                   select_by_date=select_by_date, select_by_category=select_by_category)
    except BaseException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add', response_model=ProductSchema)
async def add_product(name: str, price: float, category_name: str):
    check_category = await read_category(name=category_name)
    if check_category:
        return await write_product(name=name, price=price, category=check_category)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category does not exist')


@router.delete('/delete')
async def delete_product(product_id: int):
    check_product = await read_product(product_id=product_id)
    if check_product:
        await purge_product(product_id=product_id)
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product does not exist')
