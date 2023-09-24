import json
from typing import Any

from fast_api_example.meta_singleton import MetaSingleton
from fast_api_example.persistence.redis import redis, Redis


class RedisRepository(metaclass=MetaSingleton):

    def __init__(self, redis_instance: Redis) -> None:
        self.__redis = redis_instance

    async def get_key(self, redis_key: str) -> Any:
        str_object: str = await self.__redis.get_connection().get(redis_key)
        try:
            return json.loads(str_object)
        except (json.JSONDecodeError, TypeError):
            return str_object

    async def set_key(self, redis_key: str, redis_val: Any):
        serialized_data = json.dumps(redis_val)
        await self.__redis.get_connection().set(name=redis_key, value=serialized_data)

    async def del_key(self, redis_key: str) -> int:
        return await self.__redis.get_connection().delete(redis_key)


redis_repository = RedisRepository(redis)
