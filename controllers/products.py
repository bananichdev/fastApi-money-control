from sqlalchemy import select, insert, desc, asc, and_, or_

from models import db, products, categories

from datetime import date


async def read_products(sorting_by_price: bool, read_all: bool,
                        select_by_category: str, select_by_date: date):
    query = (select([products.c.id, products.c.name, products.c.price,
                     products.c.created_at, products.c.category_id, categories.c.name.label('category_name')])
             .select_from(products.join(categories)))
    if read_all:
        if sorting_by_price is True:
            query = query.order_by(desc(products.c.price))
        elif sorting_by_price is False:
            query = query.order_by(asc(products.c.price))
        return await db.fetch_all(query=query)
    elif select_by_category and select_by_date:
        query = query.where(and_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
        if sorting_by_price is True:
            query = query.order_by(desc(products.c.price))
        elif sorting_by_price is False:
            query = query.order_by(asc(products.c.price))
        return await db.fetch_all(query=query)
    elif select_by_category or select_by_date:
        query = query.where(or_(products.c.created_at == select_by_date, categories.c.name == select_by_category))
        if sorting_by_price is True:
            query = query.order_by(desc(products.c.price))
        elif sorting_by_price is False:
            query = query.order_by(asc(products.c.price))
        return await db.fetch_all(query=query)


async def write_product(name: str, price: float, category):
    created_at = date.today()
    query = insert(products).values(name=name, price=price, created_at=created_at, category_id=category['id'])
    product_id = await db.execute(query=query)
    content = {
        'id': product_id, 'name': name, 'price': price, 'created_at': created_at,
        'category_id': category['id'], 'category_name': category['name']
    }
    return content


async def read_product(product_id: int):
    product_query = products.select().where(products.c.id == product_id)
    return await db.fetch_one(query=product_query)


async def purge_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query=query)
