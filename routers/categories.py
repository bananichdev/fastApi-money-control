from fastapi import APIRouter, HTTPException, Response
from starlette import status

from models import CategorySchema
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError

from controllers import read_categories, write_category, read_category, purge_category

router = APIRouter()


@router.get('/', response_model=list[CategorySchema])
async def get_categories():
    return await read_categories()


@router.post('/', response_model=CategorySchema)
async def add_category(name: str):
    try:
        return await write_category(name=name)
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category already exists')


@router.delete('/', response_model=CategorySchema)
async def delete_category(name: str):
    check_category = await read_category(name=name)
    if check_category:
        try:
            await purge_category(name=name)
            return Response(status_code=status.HTTP_200_OK)
        except ForeignKeyViolationError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='There are still products in the category')
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Category does not exist')
