from os import getenv
from dotenv import load_dotenv

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine = create_async_engine(url=f"{getenv('DATABASE_URL')}", pool_size=20, max_overflow=0,
                                          pool_pre_ping=True)
        self.session = async_sessionmaker(bind=self.engine)
