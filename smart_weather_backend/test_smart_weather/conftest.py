import json

import pytest

from smart_weather import app


class SmartWeather:
    def __init__(self, client_factory):
        self.client_factory = client_factory
        self.app = None
        self.client = None

    async def async_init(self):
        self.app = await self._create_app()
        self.client = await self.client_factory(self.app)

    async def get(self, path, params=None, headers=None):
        resp = await self.client.get(path, params=params, headers=headers)
        return resp

    async def post(
            self, path, params=None, data=None, raw_data=None, headers=None,
    ):
        resp = await self.client.post(
            path, params=params, json=data, data=raw_data, headers=headers,
        )
        return resp

    @staticmethod
    def _create_app():
        res = app.create_app(
            openweathermap_api_key='TEST_KEY',
        )
        return res


@pytest.fixture
async def smart_weather(aiohttp_client):
    res = SmartWeather(client_factory=aiohttp_client)
    await res.async_init()
    return res

