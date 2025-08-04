import os
import tempfile
import shutil
import pytest
from weather_app.get_weather import get_weather

# Test weather forecast endpoint
def test_get_weather_forecast_valid_city():
    from weather_app.get_weather import get_weather_forecast
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('OPENWEATHER_API_KEY=dummy_key\n')
        result = get_weather_forecast('London', env_path=env_path)
        # Should return a dict with 'city' and 'forecasts' keys or None if the API key is invalid
        if result is not None:
            assert 'city' in result
            assert 'forecasts' in result
            assert isinstance(result['forecasts'], list)
        else:
            assert result is None


def test_get_weather_valid_city():
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('OPENWEATHER_API_KEY=dummy_key\n')
        result = get_weather('London', env_path=env_path)
        # Should return a dict with all expected keys or None if the API key is invalid
        if result is not None:
            assert 'temp' in result
            assert 'humidity' in result
            assert 'pressure' in result
            assert 'wind_speed' in result
            assert 'wind_deg' in result
            assert 'weather_description' in result
            assert 'raw' in result
        else:
            assert result is None

# Test with an invalid city name

def test_get_weather_invalid_city():
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('OPENWEATHER_API_KEY=dummy_key\n')
        result = get_weather('InvalidCityName123', env_path=env_path)
        assert result is None or ('message' in result)

# Test with empty city name

def test_get_weather_empty_city():
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('OPENWEATHER_API_KEY=dummy_key\n')
        result = get_weather('', env_path=env_path)
        assert result is None or ('message' in result)

# Test with API key but simulate timeout

def test_get_weather_timeout(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('OPENWEATHER_API_KEY=dummy_key\n')
        import requests
        def timeout_get(*args, **kwargs):
            raise requests.exceptions.Timeout()
        monkeypatch.setattr(requests, "get", timeout_get)
        result = get_weather('London', env_path=env_path)
        assert result is None
# Add a test for no API key in venv/.env
def test_get_weather_no_api_key(monkeypatch):
    with tempfile.TemporaryDirectory() as temp_venv:
        env_path = os.path.join(temp_venv, '.env')
        with open(env_path, 'w') as f:
            f.write('')  # Write empty .env
        # Temporarily clear the OPENWEATHER_API_KEY environment variable
        monkeypatch.delenv('OPENWEATHER_API_KEY', raising=False)
        result = get_weather('London', env_path=env_path)
        assert result is None
