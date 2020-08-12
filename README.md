## Умный сервис прогноза погоды 
## Тестовое задание в "Школу Будущих СТО Яндекс.Облака"

Сервис призван помогать пользователю быстро определить погоду в своем населенном пункте и советовать, а что необходимо надеть сегодня на улицу, чтобы чувствовать себя комфортно.

## Задача со звездочкой 

- **Используемый язык**: Python3, aiohttp
- **Пользовательский интерфейс**: React app
- **Форма ответа**: С сервера приходит JSON, схема ручки описана по ссылке ниже:
      См. https://github.com/Ruslan2702/smart_weather/blob/master/smart_weather_backend/smart_weather/api/schema/smart_weather.yaml#L13

- **Демонстрация**

    ![screencast](smart_weather.gif)

- **Процесс работы программы**

1) Пользователь вводит название зоны в поле ввода
2) React-приложении отправляет запрос на бекенд
3) Бекенд ходит в Openweathermap api за погодой. Далее на основании этих данных генерирует рекомендации по одежде и возвращает ответ на фронту
4) React-приложении отрисовывает полученные с бекенда данные: прогноз погоды и рекомендации по одежде

- **Обрабатываются следующие ошибки**
1) Не введена зона, Openweathermap отвечает 400
2) Такой зоны не существует, Openweathermap отвечает 404
3) Протухание токена, Openweathermap отвечает 401

- **Как запустить**

1) git clone https://github.com/Ruslan2702/smart_weather.git
2) cd smart_weather
3) docker-compose up
4) Открыть в браузере страницу http://localhost:3000/
