from fastapi import APIRouter, HTTPException, Response
from starlette import status

from models import db, Category
from models import CategorySchema

router = APIRouter()


@router.get('/get', response_model=list[CategorySchema])
async def get_categories():
    query = Category.__table__.select()
    response = await db.fetch_all(query=query)
    return response


@router.post('/add')
async def add_category(name: str):
    try:
        query = Category.__table__.insert().values(name=name)
        await db.execute(query=query)
        return Response(status_code=status.HTTP_201_CREATED)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already added')


@router.delete('/delete')
async def delete_category(name: str):
    query = Category.__table__.delete().where(Category.__table__.c.name == name)
    await db.execute(query=query)
    return Response(status_code=status.HTTP_200_OK)
