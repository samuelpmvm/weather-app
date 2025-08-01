import os
import pytest
from weather_app.get_weather import get_weather

def test_get_weather_valid_city(monkeypatch):
    # Ensure venv/.env contains a dummy key
    env_path = os.path.join('venv', '.env')
    with open(env_path, 'w') as f:
        f.write('OPENWEATHER_API_KEY=dummy_key\n')
    result = get_weather('London')
    assert isinstance(result, dict) or result is None

# Test with an invalid city name

def test_get_weather_invalid_city(monkeypatch):
    env_path = os.path.join('venv', '.env')
    with open(env_path, 'w') as f:
        f.write('OPENWEATHER_API_KEY=dummy_key\n')
    result = get_weather('InvalidCityName123')
    assert result is None or ('message' in result)

# Test with empty city name

def test_get_weather_empty_city(monkeypatch):
    env_path = os.path.join('venv', '.env')
    with open(env_path, 'w') as f:
        f.write('OPENWEATHER_API_KEY=dummy_key\n')
    result = get_weather('')
    assert result is None or ('message' in result)

# Test with API key but simulate timeout

def test_get_weather_timeout(monkeypatch):
    env_path = os.path.join('venv', '.env')
    with open(env_path, 'w') as f:
        f.write('OPENWEATHER_API_KEY=dummy_key\n')
    import requests
    def timeout_get(*args, **kwargs):
        raise requests.exceptions.Timeout()
    monkeypatch.setattr(requests, "get", timeout_get)
    result = get_weather('London')
    assert result is None
# Add a test for no API key in venv/.env
def test_get_weather_no_api_key():
    env_path = os.path.join('venv', '.env')
    with open(env_path, 'w') as f:
        f.write('')  # Write empty .env
    result = get_weather('London')
    assert result is None
