import os
from functools import wraps

from fast_api_example.persistence.mysql import database


class Transactional:
    def test_function(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        return wrapper

    def transactional_function(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await database.get_connection().commit()
            except Exception as e:
                await database.get_connection().rollback()
                raise e
            return result

        return wrapper

    def __call__(self, func):
        if os.getenv("ENV") == "test":
            return self.test_function(func)
        else:
            return self.transactional_function(func)
