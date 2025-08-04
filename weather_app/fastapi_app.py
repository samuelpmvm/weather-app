
from fastapi import FastAPI, APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from weather_app.services import WeatherService
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io

app = FastAPI()
app.mount("/static", StaticFiles(directory="weather_app/static", html=True), name="static")

weather_service = WeatherService()
router = APIRouter()

@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@router.get("/weather/current")
def current_weather(city: str):
    result = weather_service.get_current_weather(city)
    if not result:
        raise HTTPException(status_code=404, detail="Weather not found")
    return result

@router.get("/weather/forecast")
def forecast(city: str):
    result = weather_service.get_forecast(city)
    if not result:
        raise HTTPException(status_code=404, detail="Forecast not found")
    return result

@router.get("/weather/chart/{city}/{metric}")
def chart(city: str, metric: str):
    result = weather_service.get_forecast(city)
    valid_metrics = {'temperature', 'humidity', 'wind_speed', 'wind_deg'}
    if metric not in valid_metrics:
        raise HTTPException(status_code=400, detail="Invalid metric")
    if not result or not result.get('forecasts'):
        raise HTTPException(status_code=404, detail="No forecast data found")
    forecasts = result['forecasts']
    times = [entry['dt_txt'] for entry in forecasts]
    if metric == 'temperature':
        values = [entry['temp'] for entry in forecasts]
        ylabel = 'Temperature (°C)'
    elif metric == 'humidity':
        values = [entry['humidity'] for entry in forecasts]
        ylabel = 'Humidity (%)'
    elif metric == 'wind_speed':
        values = [entry['wind_speed'] for entry in forecasts]
        ylabel = 'Wind Speed (m/s)'
    elif metric == 'wind_deg':
        values = [entry['wind_deg'] for entry in forecasts]
        ylabel = 'Wind Direction (°)'
    plt.figure(figsize=(10, 5))
    plt.plot(times, values, marker='o')
    plt.title(f'{metric.replace("_", " ").title()} Forecast for {city}')
    plt.xlabel('Date/Time')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type='image/png')

app.include_router(router)
