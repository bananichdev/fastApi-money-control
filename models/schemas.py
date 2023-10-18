from pydantic import BaseModel

from datetime import datetime


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime
    category_id: int
    category_name: str

    class Config:
        from_attributes = True
