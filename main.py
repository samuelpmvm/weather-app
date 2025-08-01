
# Ask user for their desired location to lookup the weather for
from get_weather import get_weather


location = input("Enter the location for which you want to check the weather: ")

# Use the function in get_weather.py to get the weather for that location
weather_data = get_weather(location)

# print the high and low temperatures for that location
if weather_data:
    main = weather_data.get('main', {})
    temp_max = main.get('temp_max')
    temp_min = main.get('temp_min')

    if temp_max is not None and temp_min is not None:
        print(f"High: {temp_max}°C, Low: {temp_min}°C")
    else:
        print("Temperature data not available.")