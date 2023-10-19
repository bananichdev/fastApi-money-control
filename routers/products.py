from fastapi import APIRouter, Response, HTTPException, status

from models import db, categories, products, ProductSchema
from sqlalchemy import select, insert, desc, asc, and_, or_

from datetime import date

router = APIRouter()


@router.get('/get', response_model=list[ProductSchema])
async def get_products(read_all: bool, sorting_by_price_from_expensive_to_cheap: bool = None,
                       select_by_date: date = None, select_by_category: str = None):
    if read_all:
        match sorting_by_price_from_expensive_to_cheap:
            case True:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .select_from(products.join(categories)).order_by(desc(products.c.price)))
            case False:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .select_from(products.join(categories)).order_by(asc(products.c.price)))
            case _:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .select_from(products.join(categories)))
        content = await db.fetch_all(query=query)
        return content
    elif select_by_category and select_by_date:
        match sorting_by_price_from_expensive_to_cheap:
            case True:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(and_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories))).order_by(desc(products.c.price))
            case False:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(and_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories))).order_by(asc(products.c.price))
            case _:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(and_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories)))
        content = await db.fetch_all(query=query)
        return content
    elif select_by_date or select_by_category:
        match sorting_by_price_from_expensive_to_cheap:
            case True:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(or_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories))).order_by(desc(products.c.price))
            case False:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(or_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories))).order_by(asc(products.c.price))
            case _:
                query = (select([products.c.id, products.c.name, products.c.price,
                                 products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
                         .where(or_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
                         .select_from(products.join(categories)))
        content = await db.fetch_all(query=query)
        return content
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/add', response_model=ProductSchema)
async def add_product(name: str, price: float, category_name: str):
    category_query = categories.select().where(categories.c.name == category_name)
    check_category = await db.fetch_one(query=category_query)
    if check_category:
        created_at = date.today()
        query = insert(products).values(name=name, price=price, created_at=created_at, category_id=check_category['id'])
        product_id = await db.execute(query=query)
        content = {
            'id': product_id, 'name': name, 'price': price, 'created_at': created_at,
            'category_id': check_category['id'], 'category_name': check_category['name']
        }
        return content
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category does not exist')


@router.delete('/delete')
async def delete_product(product_id: int):
    product_query = products.select().where(products.c.id == product_id)
    check_product = await db.fetch_one(query=product_query)
    if check_product:
        query = products.delete().where(products.c.id == product_id)
        await db.execute(query=query)
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Product does not exist')
