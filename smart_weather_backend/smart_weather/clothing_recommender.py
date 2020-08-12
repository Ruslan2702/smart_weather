from abc import ABC, abstractmethod
import typing as tp

from smart_weather.clients.open_weather_map import OpenMapForecastResponse

RainsGroup: str = 'Rain'

class AbstractHandler(ABC):
    """
    The chain handler (Chain of responsibilities pattern)
    """
    @abstractmethod
    def __init__(self, handler = None):
        pass

    @abstractmethod
    def handle(
            self, forecast_result: OpenMapForecastResponse,
    ) -> tp.Optional[str]:
        pass

    @abstractmethod
    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        pass


class Handler(AbstractHandler):
    _next_handler: AbstractHandler = None
    recommendation: str = ''

    def __init__(self, handler: AbstractHandler = None) -> AbstractHandler:
        super().__init__(handler)
        if handler:
            self._next_handler = handler

    def handle(
            self, forecast_result: OpenMapForecastResponse,
    ) -> str:
        print('HANDLE HERE :', self, forecast_result.current_temp)

        if self._next_handler:
            if self.check_conditions(forecast_result):
                print('APPEND RECOMMENT', self.recommendation)
                return self._next_handler.handle(
                    forecast_result,
                ) + self.recommendation
            else:
                return self._next_handler.handle(forecast_result)

        return ''

    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        return False


class RainHandler(Handler):
    """
    If it rains, recommend to take umbrella
    """
    recommendation: str = 'Do not forget to take an umbrella. '

    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        print('CHECK HERE :', self, forecast_result.current_temp)
        return forecast_result.group == RainsGroup


class WinterJacketHandler(Handler):
    recommendation: str = 'Wear winter jacket. '

    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        print('CHECK HERE :', self, forecast_result.current_temp)
        return forecast_result.current_temp < 10


class ThinJacketHandler(Handler):
    recommendation: str = 'Take thin jacket. '

    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        print('CHECK HERE :', self, forecast_result.current_temp)
        return 10 < forecast_result.current_temp < 20


class NoJacketHandler(Handler):
    recommendation: str = 'Do not take your jacket with you. '

    def check_conditions(
            self, forecast_result: OpenMapForecastResponse,
    ) -> bool:
        print('CHECK HERE :', self, forecast_result.current_temp)
        return forecast_result.current_temp > 20


chain: tp.List[tp.Type[Handler]] = [
    NoJacketHandler, ThinJacketHandler, WinterJacketHandler, RainHandler,
]


async def match_recommendations(forecast_result: OpenMapForecastResponse):
    result_handler: Handler = Handler()
    for handler in chain:
        result_handler = handler(result_handler)

    return result_handler.handle(forecast_result).strip()
