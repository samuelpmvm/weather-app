
# Ask user for their desired location to lookup the weather for
import argparse
import logging
from weather_app.get_weather import get_weather, get_weather_forecast

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Weather CLI: Get current weather or forecast for a city.")
    parser.add_argument("city", type=str, help="City name to look up weather for.")
    parser.add_argument("--forecast", action="store_true", help="Get 5-day/3-hour weather forecast instead of current weather.")
    args = parser.parse_args()

    if args.forecast:
        result = get_weather_forecast(args.city)
        if result:
            city = result.get('city', {}).get('name', args.city)
            print(f"Weather forecast for {city}:")
            for entry in result['forecasts'][:5]:  # Show first 5 forecast entries
                print(f"{entry['dt_txt']}: {entry['temp']}°C, {entry['weather_description']}, Humidity: {entry['humidity']}%, Wind: {entry['wind_speed']} m/s")
        else:
            print("Could not retrieve forecast data.")
    else:
        weather_data = get_weather(args.city)
        if weather_data:
            print(f"Current weather in {args.city}:")
            print(f"Temperature: {weather_data['temp']}°C (min: {weather_data['temp_min']}°C, max: {weather_data['temp_max']}°C)")
            print(f"Description: {weather_data['weather_description']}")
            print(f"Humidity: {weather_data['humidity']}%")
            print(f"Pressure: {weather_data['pressure']} hPa")
            print(f"Wind: {weather_data['wind_speed']} m/s, {weather_data['wind_deg']}°")
        else:
            print("Could not retrieve weather data.")

if __name__ == "__main__":
    main()