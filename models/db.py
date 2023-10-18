from os import environ

from sqlalchemy import create_engine, MetaData

from databases import Database

POSTGRESQL_DB_URL = environ.get('FASTAPI_DB_URL')

engine = create_engine(
    POSTGRESQL_DB_URL,
    future=True
)

db = Database(POSTGRESQL_DB_URL)

metadata = MetaData()
