from fastapi import APIRouter, HTTPException, Response
from starlette import status

from models import db, categories, CategorySchema
from asyncpg.exceptions import UniqueViolationError

router = APIRouter()


@router.get('/get', response_model=list[CategorySchema])
async def get_categories():
    query = categories.select()
    content = await db.fetch_all(query=query)
    return content


@router.post('/add', response_model=CategorySchema)
async def add_category(name: str):
    try:
        query = categories.insert()
        category_id = await db.execute(query=query, values={'name': name})
        content = {'id': category_id, 'name': name}
        return content
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exists')


@router.delete('/delete')
async def delete_category(name: str):
    category_query = categories.select().where(categories.c.name == name)
    check_category = await db.fetch_one(query=category_query)
    if check_category:
        query = categories.delete().where(categories.c.name == name)
        await db.execute(query=query)
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category does not exist')
