from fastapi import FastAPI

from app.routes import router

app = FastAPI()

app.include_router(router, tags=["currencies"])
app.include_router(router, tags=["exchange_rates"])

