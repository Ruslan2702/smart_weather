import aiohttp


class BaseError(Exception):
    pass


class UnauthorizedError(BaseError):
    """
    401 from openweathermap api was handled
    """
    pass


class ZoneNotFoundError(BaseError):
    """
    404 from openweathermap api was handled
    """
    pass


class OpenMapForecastResponse:
    def __init__(self, weather_service_response: dict):
        self.description = weather_service_response['weather'][0]['description']
        self.group = weather_service_response['weather'][0]['main']

        self.current_temp = weather_service_response['main']['temp']
        self.feels_like = weather_service_response['main']['feels_like']


class OpenWeatherMapClient:
    """
    Client to invoke openweathermap api
    """

    def __init__(self, api_key: str):
        self.API_KEY = api_key

    async def forecast(self, city: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url='https://api.openweathermap.org/data/2.5/weather',
                params={
                    'q': city,
                    'appid': self.API_KEY,
                    'units': 'metric',
                }
            ) as response:
                await self.raise_for_status(response)
                resp_body = await response.json()
                return OpenMapForecastResponse(resp_body)

    @staticmethod
    async def raise_for_status(response):
        resp_body = await response.json()
        if response.status == 200:
            return
        elif response.status == 401:
            raise UnauthorizedError()
        elif response.status == 404:
            raise ZoneNotFoundError()
        else:
            raise BaseError(f'Unhandled error on status code {response.status}')
