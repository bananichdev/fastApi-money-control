from pydantic import BaseModel

from datetime import date


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    created_at: date
    category_id: int
    category_name: str

    class Config:
        from_attributes = True
