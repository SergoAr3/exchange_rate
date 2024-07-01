import uvicorn

from fastapi import FastAPI

from app.handlers import router

# from contextlib import asynccontextmanager
# from loguru import logger
# from asyncpg.exceptions import UniqueViolationError
# from sqlalchemy.exc import IntegrityError
# from app.db.config import Database, Base

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     database = Database()
#     engine = database.engine
#     try:
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#     except (IntegrityError, UniqueViolationError) as e:
#         logger.warning('duplicate key value violates unique constraint "pg_class_relname_nsp_index"')
#     yield
#     engine.dispose()

# app = FastAPI(lifespan=lifespan)

app = FastAPI(docs_url="/")

app.include_router(router, tags=["currencies"])

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, workers=2, log_level="info")
