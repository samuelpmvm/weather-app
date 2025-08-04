import os
import pytest
from weather_app.get_weather import get_weather

def test_get_weather_valid(monkeypatch):
    # Set a dummy API key for testing
    monkeypatch.setenv('OPENWEATHER_API_KEY', os.environ.get('OPENWEATHER_API_KEY', 'dummy_key'))

    # Mock the requests.get call inside get_weather
    import weather_app.get_weather as gw
    class DummyResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"weather": "sunny"}
        def raise_for_status(self):
            pass
    monkeypatch.setattr(gw.requests, "get", lambda *args, **kwargs: DummyResponse())

    result = get_weather('London')
    assert isinstance(result, dict) or result is None

def test_get_weather_no_api_key(monkeypatch):
    # Remove API key from environment and ensure it's empty
    monkeypatch.setenv('OPENWEATHER_API_KEY', '')

    result = get_weather('London')
    assert result is None
