import os
from dotenv import load_dotenv
import requests


# A function that uses the requests library to make a GET request to
# the OpenWeatherMap API for certain location

def get_weather(location):
    # Always load environment variables from venv/.env
    load_dotenv(dotenv_path=os.path.join('venv', '.env'))
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        print("Error: OPENWEATHER_API_KEY not found in venv/.env.")
        return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to retrieve weather data for {location}.")
        return None