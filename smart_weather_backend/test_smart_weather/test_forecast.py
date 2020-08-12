import pytest

import aiohttp
from test_smart_weather.conftest import SmartWeather
from smart_weather.clients import open_weather_map


@pytest.fixture()
async def patch_session(monkeypatch):
    async def _wrapper():
        async def mock_forecast(*args, **kwargs):
            assert args[1] == 'Moscow'

            return open_weather_map.OpenMapForecastResponse({
                'weather': [
                    {
                        'main': 'Rain',
                        'description': 'scattered clouds',
                    }
                ],
                'main': {
                    'temp': 14,
                    'feels_like': 10.82,
                },
            })
        monkeypatch.setattr(
            open_weather_map.OpenWeatherMapClient, 'forecast', mock_forecast,
        )
    return _wrapper


async def test_happy_path(
        smart_weather: SmartWeather,
        patch_session,
):
    await patch_session()

    response = await smart_weather.post(
        '/v1/forecast',
        data={
            'zone_name': 'Moscow',
        },
    )
    assert response.status == 200
    resp_body = await response.json()
    assert resp_body == {
        'clothing_recommendations': 'Take thin jacket. '
                                    'Do not forget to take an umbrella.',
        'weather': {
            'comment': 'scattered clouds',
            'parameters': 'Rain',
            'current_temp': 14,
            'feels_like': 10.82,
        }
    }


async def test_no_zone_name(
        smart_weather: SmartWeather,
        patch_session,
):
    await patch_session()

    response = await smart_weather.post(
        '/v1/forecast',
        data={},
    )
    assert response.status == 400
    resp_body = await response.json()
    assert resp_body == {
        'code': 'Bad request',
        'message': 'No city in request body',
    }
