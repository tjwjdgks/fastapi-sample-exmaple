import json

import aiohttp

from fast_api_example.meta_singleton import MetaSingleton


class AsyncHttpClient(metaclass=MetaSingleton):
    async def get_response(self, url, method, header, data, type_name="json"):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            if method == "GET":
                async with session.get(url=url, headers=header, data=data) as resp:
                    return resp.status, await self.convert_to(type_name, resp)
            elif method == "POST":
                async with session.post(url=url, headers=header, data=data) as resp:
                    return resp.status, await self.convert_to(type_name, resp)
            elif method == "PUT":
                async with session.put(url=url, headers=header, data=data) as resp:
                    return resp.status, await self.convert_to(type_name, resp)

    async def convert_to(self, type_name: str, response: aiohttp.ClientResponse):
        if type_name == "text":
            return await self.convert_to_text(response)
        return await self.convert_to_json(response)

    async def convert_to_text(self, response: aiohttp.ClientResponse) -> str:
        return await response.text()

    async def convert_to_json(self, response: aiohttp.ClientResponse) -> dict:
        response_text = await response.text()
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            raise ValueError("api convert to json.. json decode error")


async_requests = AsyncHttpClient()
