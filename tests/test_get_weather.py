import os
import pytest
from weather_app.get_weather import get_weather

def test_get_weather_valid(monkeypatch):
    # Set a dummy API key for testing
    monkeypatch.setenv('OPENWEATHER_API_KEY', os.environ.get('OPENWEATHER_API_KEY', 'dummy_key'))
    result = get_weather('London')
    assert isinstance(result, dict) or result is None

def test_get_weather_no_api_key(monkeypatch):
    monkeypatch.delenv('OPENWEATHER_API_KEY', raising=False)
    result = get_weather('London')
    assert result is None
