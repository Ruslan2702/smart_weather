import os

from aiohttp import web
import asyncio
import aiohttp_cors

from smart_weather.api import forecast
from smart_weather.api import ping


async def create_app(openweathermap_api_key: str = None):
    app = web.Application()
    app.add_routes([web.get('/ping', ping.handle)])

    app['OPENWEATHERMAP_API_KEY'] = openweathermap_api_key

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    resource = cors.add(app.router.add_resource('/v1/forecast{slash:/?}'))
    cors.add(resource.add_route("POST", forecast.handle))

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
