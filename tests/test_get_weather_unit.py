import os
import pytest
from weather_app.get_weather import get_weather, get_weather_forecast

def test_get_weather_valid(monkeypatch):
    monkeypatch.setenv('OPENWEATHER_API_KEY', 'dummy_key')
    import weather_app.get_weather as gw
    class DummyResponse:
        def __init__(self):
            self.status_code = 200
        def json(self):
            return {"weather": [{"description": "sunny"}]}
        def raise_for_status(self):
            pass
    monkeypatch.setattr(gw.requests, "get", lambda *args, **kwargs: DummyResponse())
    result = get_weather('London')
    assert isinstance(result, dict) or result is None

def test_get_weather_no_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv('OPENWEATHER_API_KEY', raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text("")
    result = get_weather("Lisboa", env_path=str(env_path))
    assert result is None

def test_get_weather_forecast_no_api_key(monkeypatch, tmp_path):
    monkeypatch.delenv('OPENWEATHER_API_KEY', raising=False)
    env_path = tmp_path / ".env"
    env_path.write_text("")
    result = get_weather_forecast("Lisboa", env_path=str(env_path))
    assert result is None

def test_get_weather_forecast_empty_list(monkeypatch, tmp_path):
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): return {"list": []}
    def dummy_get(*a, **kw): return DummyResponse()
    import weather_app.get_weather as gw
    monkeypatch.setenv('OPENWEATHER_API_KEY', 'dummy')
    monkeypatch.setattr(gw.requests, "get", dummy_get)
    env_path = tmp_path / ".env"
    env_path.write_text("OPENWEATHER_API_KEY=dummy\n")
    result = get_weather_forecast("Lisboa", env_path=str(env_path))
    assert result["forecasts"] == []

def test_get_weather_forecast_no_list(monkeypatch, tmp_path):
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): return {}
    def dummy_get(*a, **kw): return DummyResponse()
    import weather_app.get_weather as gw
    monkeypatch.setenv('OPENWEATHER_API_KEY', 'dummy')
    monkeypatch.setattr(gw.requests, "get", dummy_get)
    env_path = tmp_path / ".env"
    env_path.write_text("OPENWEATHER_API_KEY=dummy\n")
    result = get_weather_forecast("Lisboa", env_path=str(env_path))
    assert result["forecasts"] == []
