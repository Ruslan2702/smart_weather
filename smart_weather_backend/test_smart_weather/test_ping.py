from test_smart_weather.conftest import SmartWeather


async def test_ping(smart_weather: SmartWeather):
    response = await smart_weather.get('/ping')
    assert response.status == 200
