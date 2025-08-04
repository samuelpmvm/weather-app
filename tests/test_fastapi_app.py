import pytest
from fastapi.testclient import TestClient
from weather_app.fastapi_app import app

@pytest.fixture
def client():
    return TestClient(app)

def test_current_weather_success(monkeypatch, client):
    def mock_get_current_weather(*args, **kwargs):
        return {'temp': 20, 'temp_min': 18, 'temp_max': 22, 'humidity': 60, 'pressure': 1012, 'wind_speed': 5, 'wind_deg': 180, 'weather_description': 'clear sky', 'raw': {}}
    import weather_app.fastapi_app as fastapi_app
    monkeypatch.setattr(fastapi_app.weather_service, 'get_current_weather', mock_get_current_weather)
    resp = client.get('/weather/current?city=Lisboa')
    assert resp.status_code == 200
    assert resp.json()['temp'] == 20

def test_current_weather_not_found(monkeypatch, client):
    def mock_get_current_weather(*args, **kwargs):
        return None
    import weather_app.fastapi_app as fastapi_app
    monkeypatch.setattr(fastapi_app.weather_service, 'get_current_weather', mock_get_current_weather)
    resp = client.get('/weather/current?city=Nowhere')
    assert resp.status_code == 404

def test_forecast_success(monkeypatch, client):
    def mock_get_forecast(*args, **kwargs):
        city = args[1] if len(args) > 1 else args[0] if args else 'city'
        return {'city': {'name': city}, 'forecasts': [
            {'dt_txt': '2025-08-04 12:00', 'temp': 20, 'humidity': 60, 'wind_speed': 5, 'wind_deg': 180},
            {'dt_txt': '2025-08-04 15:00', 'temp': 22, 'humidity': 55, 'wind_speed': 6, 'wind_deg': 190},
        ]}
    import weather_app.fastapi_app as fastapi_app
    monkeypatch.setattr(fastapi_app.weather_service, 'get_forecast', mock_get_forecast)
    resp = client.get('/weather/forecast?city=Lisboa')
    assert resp.status_code == 200
    assert 'forecasts' in resp.json()

@pytest.mark.parametrize("metric", ["temperature", "humidity", "wind_speed", "wind_deg"])
def test_chart_success(monkeypatch, client, metric):
    def mock_get_forecast(*args, **kwargs):
        city = args[1] if len(args) > 1 else args[0] if args else 'city'
        return {'city': {'name': city}, 'forecasts': [
            {'dt_txt': '2025-08-04 12:00', 'temp': 20, 'humidity': 60, 'wind_speed': 5, 'wind_deg': 180},
            {'dt_txt': '2025-08-04 15:00', 'temp': 22, 'humidity': 55, 'wind_speed': 6, 'wind_deg': 190},
        ]}
    import weather_app.fastapi_app as fastapi_app
    monkeypatch.setattr(fastapi_app.weather_service, 'get_forecast', mock_get_forecast)
    resp = client.get(f'/weather/chart/Lisboa/{metric}')
    assert resp.status_code == 200
    assert resp.headers['content-type'] == 'image/png'

def test_chart_invalid_metric(monkeypatch, client):
    def mock_get_forecast(*args, **kwargs):
        city = args[1] if len(args) > 1 else args[0] if args else 'city'
        return {'city': {'name': city}, 'forecasts': [
            {'dt_txt': '2025-08-04 12:00', 'temp': 20, 'humidity': 60, 'wind_speed': 5, 'wind_deg': 180},
        ]}
    import weather_app.fastapi_app as fastapi_app
    monkeypatch.setattr(fastapi_app.weather_service, 'get_forecast', mock_get_forecast)
    resp = client.get('/weather/chart/Lisboa/invalid')
    assert resp.status_code == 400

def test_docs_endpoint(client):
    resp = client.get('/docs')
    assert resp.status_code == 200
    assert b"Swagger UI" in resp.content
