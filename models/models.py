from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String, Date

from .db import metadata

from datetime import date


categories = Table(
    "categories",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, unique=True, nullable=False, index=True)
)

products = Table(
    "products",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, nullable=False, index=True),
    Column('price', Float, nullable=False, index=True),
    Column('created_at', Date, nullable=False, index=True, default=date.today()),
    Column('category_id', Integer, ForeignKey('categories.id'))
)
