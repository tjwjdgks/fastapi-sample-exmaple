import json

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request

from fast_api_example.account.router.account_router import account_router
from fast_api_example.lib.exception_handler import default_error_handler
from fast_api_example.lib.middleware import SQLAlchemyMiddleware, LogMiddleware
from fast_api_example.persistence.mysql import database

app = FastAPI(title="example API")

app.include_router(account_router)
app.add_middleware(SQLAlchemyMiddleware)
app.add_middleware(LogMiddleware)
app.add_exception_handler(Exception, default_error_handler)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def hello(request: Request):
    raise ValueError("test", "test-mesage")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
