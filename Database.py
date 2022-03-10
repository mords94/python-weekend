
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from config import DATABASE_URL


class Database:
    def __init__(self):
        self.engine = create_engine(
            DATABASE_URL,
            echo=False,
            poolclass=NullPool
        )
