from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from databases import Database

POSTGRESQL_DB_URL = environ.get('FASTAPI_DB_URL')

engine = create_engine(
    POSTGRESQL_DB_URL,
    future=True
)

db = Database(POSTGRESQL_DB_URL)

Base = declarative_base()
