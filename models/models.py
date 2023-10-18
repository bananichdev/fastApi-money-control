from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .db import Base

from datetime import datetime


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    products = relationship('Product', back_populates='category')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, index=True, default=datetime.now())
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')

    @hybrid_property
    def category_name(self):
        return self.category.name if self.category else None
