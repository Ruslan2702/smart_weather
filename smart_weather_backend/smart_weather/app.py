import os

from aiohttp import web
import asyncio

from smart_weather.api import forecast
from smart_weather.api import ping


async def create_app(openweathermap_api_key: str = None):
    app = web.Application()
    app.add_routes([
        web.get('/ping', ping.handle),
        web.post('/v1/forecast{slash:/?}', forecast.handle),
    ])

    app['OPENWEATHERMAP_API_KEY'] = openweathermap_api_key

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(
        create_app(openweathermap_api_key=os.environ['OPENWEATHERMAP_API_KEY']),
    )
    web.run_app(
        app,
        host=os.environ.get('HOST', '0.0.0.0'),
        port=os.environ.get('PORT', 8080),
    )
