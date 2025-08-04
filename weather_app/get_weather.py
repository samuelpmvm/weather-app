import os
import logging
from dotenv import load_dotenv
import requests
import requests_cache

def get_weather_forecast(location: str, env_path: str = os.path.join('venv', '.env')) -> dict | None:
    """Fetch 5-day/3-hour weather forecast for a location, with caching."""
    logging.basicConfig(level=logging.INFO)
    load_dotenv(dotenv_path=env_path)
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        logging.error(f"OPENWEATHER_API_KEY not found in {env_path}.")
        return None
    # Cache all requests for 10 minutes
    requests_cache.install_cache('weather_cache', expire_after=600)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred for {location}: {err}")
        return None
    data = response.json()
    forecasts = []
    for entry in data.get('list', []):
        main = entry.get('main', {})
        wind = entry.get('wind', {})
        weather_list = entry.get('weather', [{}])
        weather_desc = weather_list[0].get('description') if weather_list else None
        forecasts.append({
            'dt_txt': entry.get('dt_txt'),
            'temp': main.get('temp'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'wind_speed': wind.get('speed'),
            'wind_deg': wind.get('deg'),
            'weather_description': weather_desc,
        })
    return {'city': data.get('city', {}), 'forecasts': forecasts}

# A function that uses the requests library to make a GET request to
# the OpenWeatherMap API for certain location

def get_weather(location: str, env_path: str = os.path.join('venv', '.env')) -> dict | None:
    logging.basicConfig(level=logging.INFO)
    load_dotenv(dotenv_path=env_path)
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        logging.error(f"OPENWEATHER_API_KEY not found in {env_path}.")
        return None
    # Cache all requests for 10 minutes
    requests_cache.install_cache('weather_cache', expire_after=600)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logging.error(f"Request timed out for location: {location}.")
        return None
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred for {location}: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"Error occurred for {location}: {err}")
        return None
    data = response.json()
    # Extract main weather data
    main = data.get('main', {})
    wind = data.get('wind', {})
    weather_list = data.get('weather', [{}])
    weather_desc = weather_list[0].get('description') if weather_list else None
    return {
        'temp': main.get('temp'),
        'temp_min': main.get('temp_min'),
        'temp_max': main.get('temp_max'),
        'humidity': main.get('humidity'),
        'pressure': main.get('pressure'),
        'wind_speed': wind.get('speed'),
        'wind_deg': wind.get('deg'),
        'weather_description': weather_desc,
        'raw': data  # include full response for advanced use
    }
