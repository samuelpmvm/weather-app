from weather_app.config import settings
from weather_app.get_weather import get_weather, get_weather_forecast

class WeatherService:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENWEATHER_API_KEY

    def get_current_weather(self, city: str):
        # You can add logic here to use self.api_key if needed
        return get_weather(city)

    def get_forecast(self, city: str):
        # You can add logic here to use self.api_key if needed
        return get_weather_forecast(city)
