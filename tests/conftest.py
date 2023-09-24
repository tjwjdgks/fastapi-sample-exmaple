from uuid import uuid4

import pytest
import asyncio

import pytest_asyncio

from fast_api_example.lib.context import app_context
from fast_api_example.persistence.mysql import database
from fastapi.testclient import TestClient
from fast_api_example.main import app


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def set_context_var():
    session_id = str(uuid4())
    session_context = app_context.set_session_context(session_id=session_id)
    yield session_context


@pytest_asyncio.fixture
async def db_connection(set_context_var):
    try:
        yield
    except Exception as e:
        print("Exception in db_connection fixture")
        raise e
    finally:
        await database.get_connection().rollback()
        await database.get_connection().remove()
        await database.disconnect()


@pytest.fixture(scope="session")
def get_test_client():
    client = TestClient(app)
    return client
