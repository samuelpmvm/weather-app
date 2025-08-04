import os
import io
import pytest
from weather_app.chart_api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("metric,expected_label", [
    ("temperature", "Temperature (°C)"),
    ("humidity", "Humidity (%)"),
    ("wind_speed", "Wind Speed (m/s)"),
    ("wind_deg", "Wind Direction (°)")
])
def test_chart_metrics(client, monkeypatch, metric, expected_label):
    def mock_get_weather_forecast(city, env_path=None):
        return {
            'city': {'name': city},
            'forecasts': [
                {'dt_txt': '2025-08-04 12:00', 'temp': 20, 'humidity': 60, 'wind_speed': 5, 'wind_deg': 180},
                {'dt_txt': '2025-08-04 15:00', 'temp': 22, 'humidity': 55, 'wind_speed': 6, 'wind_deg': 190},
            ]
        }
    import weather_app.chart_api as chart_api
    monkeypatch.setattr(chart_api, 'get_weather_forecast', mock_get_weather_forecast)
    rv = client.get(f'/chart/Lisboa/{metric}')
    assert rv.status_code == 200
    assert rv.mimetype == 'image/png'
    assert rv.data[:8] == b'\x89PNG\r\n\x1a\n'

def test_chart_invalid_metric(client, monkeypatch):
    def mock_get_weather_forecast(city, env_path=None):
        return {'city': {'name': city}, 'forecasts': [
            {'dt_txt': '2025-08-04 12:00', 'temp': 20, 'humidity': 60, 'wind_speed': 5, 'wind_deg': 180}
        ]}
    import weather_app.chart_api as chart_api
    monkeypatch.setattr(chart_api, 'get_weather_forecast', mock_get_weather_forecast)
    rv = client.get('/chart/Lisboa/invalid')
    assert rv.status_code == 400
    assert b'Invalid metric' in rv.data
