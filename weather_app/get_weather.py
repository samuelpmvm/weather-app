import os
import logging
from dotenv import load_dotenv
import requests

# A function that uses the requests library to make a GET request to
# the OpenWeatherMap API for certain location

def get_weather(location: str) -> dict | None:
    logging.basicConfig(level=logging.INFO)
    # Always load environment variables from venv/.env
    load_dotenv(dotenv_path=os.path.join('venv', '.env'))
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        logging.error("OPENWEATHER_API_KEY not found in venv/.env.")
        return None
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
    return response.json()
