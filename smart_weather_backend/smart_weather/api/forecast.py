import json
import typing as tp

from aiohttp import web

from smart_weather.clients import open_weather_map
from smart_weather import clothing_recommender


async def parse_request_zone_name(request: web.Request) -> tp.Optional[str]:
    data = await request.json()
    try:
        return data['zone_name']
    except KeyError:
        raise web.HTTPBadRequest(
            text=json.dumps({
                'code': 'Bad request',
                'message': 'No city in request body',
            }),
            content_type='application/json',
        )


async def fetch_weather_forecast(
    open_weather_map_client: open_weather_map.OpenWeatherMapClient,
    zone_name: str,
) -> tp.Optional[open_weather_map.OpenMapForecastResponse]:
    try:
        return await open_weather_map_client.forecast(zone_name)
    except open_weather_map.BadRequest:
        raise web.HTTPUnauthorized(
           text=json.dumps({
                'code': 'Bad Request',
                'message': 'Zone name is empty',
            }),
           content_type='application/json',
        )
    except open_weather_map.UnauthorizedError:
        raise web.HTTPUnauthorized(
           text=json.dumps({
                'code': 'Unauthorized',
                'message': 'API token was expired',
            }),
           content_type='application/json',
        )
    except open_weather_map.ZoneNotFoundError:
        raise web.HTTPNotFound(
           text=json.dumps({
                'code': 'Not Found',
                'message': f'Zone {zone_name} was not found',
            }),
           content_type='application/json',
        )


async def build_response(
        forecast: open_weather_map.OpenMapForecastResponse,
        clothing_recommendations: str,
) -> web.Response:
    return web.json_response({
        'weather': {
            'comment': forecast.description,
            'parameters': forecast.group,
            'current_temp': forecast.current_temp,
            'feels_like': forecast.feels_like,
        },
        'clothing_recommendations': clothing_recommendations,
    })


async def handle(request: web.Request) -> web.Response:
    zone_name = await parse_request_zone_name(request)

    open_weather_map_client = open_weather_map.OpenWeatherMapClient(
        request.app['OPENWEATHERMAP_API_KEY'],
    )
    forecast = await fetch_weather_forecast(open_weather_map_client, zone_name)

    clothing_recommendations: str = (
        await clothing_recommender.match_recommendations(forecast)
    )
    return await build_response(forecast, clothing_recommendations)
