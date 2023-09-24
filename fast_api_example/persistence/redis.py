import os

import aioredis
from .database import Database


class Redis(Database):
    def __init__(self) -> None:
        self.__redis_host = os.getenv("REDIS_HOST")
        self.__redis_port = int(os.getenv("REDIS_PORT", -1))
        self.__redis_password = os.getenv("REDIS_PASSWORD")
        self.__redis_url = f"redis://{self.__redis_host}"
        self.__redis_instance = aioredis.from_url(
            self.__redis_url,
            password=self.__redis_password,
            port=self.__redis_port,
            decode_responses=True,
        )

    def get_connection(self):
        return self.__redis_instance

    def get_metadata(self):
        return None

    async def scan_items_async(self, key: str, pattern: str, count: int = 10):
        items = []
        async for item in self.__redis_instance.sscan_iter(
            name=key, match=pattern, count=count
        ):
            items.append(item)
        return items


redis = Redis()
