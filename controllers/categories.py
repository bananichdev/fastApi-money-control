from models import db, categories


async def read_categories():
    query = categories.select()
    return await db.fetch_all(query=query)


async def write_category(name: str):
    query = categories.insert()
    category_id = await db.execute(query=query, values={'name': name})
    content = {'id': category_id, 'name': name}
    return content


async def read_category(name: str):
    category_query = categories.select().where(categories.c.name == name)
    return await db.fetch_one(query=category_query)


async def purge_category(name: str):
    query = categories.delete().where(categories.c.name == name)
    await db.execute(query=query)
