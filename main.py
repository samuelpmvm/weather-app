
# Ask user for their desired location to lookup the weather for
import logging
from weather_app.get_weather import get_weather


logging.basicConfig(level=logging.INFO)
location: str = input("Enter the location for which you want to check the weather: ")

# Use the function in get_weather.py to get the weather for that location
weather_data: dict | None = get_weather(location)

# print the high and low temperatures for that location
if weather_data:
    main: dict = weather_data.get('main', {})
    temp_max: float | None = main.get('temp_max')
    temp_min: float | None = main.get('temp_min')

    if temp_max is not None and temp_min is not None:
        logging.info(f"High: {temp_max}°C, Low: {temp_min}°C")
    else:
        logging.warning("Temperature data not available.")