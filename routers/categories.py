from fastapi import APIRouter, HTTPException, Response
from starlette import status

from models import CategorySchema
from asyncpg.exceptions import UniqueViolationError

from controllers import read_categories, write_category, read_category, purge_category

router = APIRouter()


@router.get('/get', response_model=list[CategorySchema])
async def get_categories():
    return await read_categories()


@router.post('/add', response_model=CategorySchema)
async def add_category(name: str):
    try:
        return await write_category(name=name)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exists')


@router.delete('/delete')
async def delete_category(name: str):
    check_category = await read_category(name=name)
    if check_category:
        await purge_category(name=name)
        return Response(status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category does not exist')
