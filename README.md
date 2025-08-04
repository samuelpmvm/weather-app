# Weather App

[![Weather API Test](https://github.com/samuelpmvm/weather-app/actions/workflows/test-weather-api.yml/badge.svg)](https://github.com/samuelpmvm/weather-app/actions)
[![Docker Build & Test](https://github.com/samuelpmvm/weather-app/actions/workflows/Docker-CI.yml/badge.svg)](https://github.com/samuelpmvm/weather-app/actions/workflows/Docker-CI.yml)
[![codecov](https://codecov.io/gh/samuelpmvm/weather-app/branch/main/graph/badge.svg)](https://codecov.io/gh/samuelpmvm/weather-app)

This is a simple Python app that fetches weather data for a given location using the OpenWeatherMap API.

## Technologies Used

- Python 3
- requests (HTTP library)
- python-dotenv (environment variable management)
- OpenWeatherMap API
- GitHub Actions (for CI testing)
- FastAPI (for REST API)
- pytest & pytest-cov (for testing and coverage)
- Docker (for containerized deployment)

## Features

- Fetches current weather data for any city using OpenWeatherMap
- Secure API key management via `.env` file in `venv`
- REST API for current weather and 5-day/3-hour forecast
- Chart endpoints for temperature, humidity, wind speed, wind direction (PNG)
- Interactive API docs at `/docs`
- Minimal web frontend for chart visualization
- Automated API test workflow with GitHub Actions
- Automated Docker build & test workflow with GitHub Actions
- Automated test coverage reporting (see badge above)

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   You can use the `get_weather.py` functions in your own scripts, or run `main.py` if provided.
   Example usage in Python:
   ```python
   from get_weather import get_weather
   print(get_weather('London'))
   ```

## API Key Setup

The recommended way to provide your OpenWeatherMap API key is to create a `.env` file inside your `venv` folder:

```bash
echo "OPENWEATHER_API_KEY=your_api_key_here" > venv/.env
```

The required packages will be installed automatically from `requirements.txt`.

Your app will automatically load the API key from `venv/.env` when you run it.

Alternatively, you can set the environment variable manually:
```bash
export OPENWEATHER_API_KEY='your_api_key_here'
```
This can be added to your `.bashrc`, `.zshrc`, or run in your terminal before starting the app.

## Test Coverage

This project uses [pytest](https://docs.pytest.org/) and [pytest-cov](https://pytest-cov.readthedocs.io/) for automated testing and coverage reporting.
Coverage is checked automatically in CI on every push and pull request.

To check coverage locally:
```bash
pytest --cov=weather_app --cov-report=term-missing
```

## Notes
- Make sure to keep your API key secure and never commit it to version control.
- The virtual environment directory (`venv`) is ignored by git (see `.gitignore`).

## Weather App (FastAPI Version)

### Features
- REST API for current weather and 5-day/3-hour forecast
- Chart endpoints for temperature, humidity, wind speed, wind direction (PNG)
- Interactive API docs at `/docs`
- Ready for frontend or CLI integration

### Running the API

```bash
uvicorn weather_app.fastapi_app:app --reload
```

### API Endpoints

- `GET /weather/current?city=Lisboa` — Current weather for a city
- `GET /weather/forecast?city=Lisboa` — 5-day/3-hour forecast for a city
- `GET /weather/chart/{city}/{metric}` — Chart image for a metric (`temperature`, `humidity`, `wind_speed`, `wind_deg`)
- `GET /docs` — Interactive API documentation (Swagger UI)

### Example Usage

- Get current weather:
  ```
  curl "http://127.0.0.1:8000/weather/current?city=Lisboa"
  ```
- Get a temperature chart:
  ```
  curl "http://127.0.0.1:8000/weather/chart/Lisboa/temperature" --output temp.png
  ```

### Running Tests

```bash
pytest
```

---

## Web Frontend

A minimal web frontend is included for quick chart visualization.

### How to use

1. Start the FastAPI server:
   ```bash
   uvicorn weather_app.fastapi_app:app --reload
   ```
2. Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
3. Enter a city and select a metric to view the chart.

This frontend is located at [`weather_app/static/index.html`](weather_app/static/index.html) and is served automatically by FastAPI.


## Docker Deployment

### Using Docker Compose (Recommended)

1. Create a `.env` file in the project root with your OpenWeatherMap API key. Docker Compose will automatically load environment variables from this file using the `env_file` setting:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```


2. Build and run the app:
   ```bash
   docker-compose up --build -d
   # No need to set OPENWEATHER_API_KEY manually; Compose loads it from .env
   ```

3. The app will be available at [http://localhost:8000](http://localhost:8000).

4. To stop the app:
   ```bash
   docker-compose down
   ```

### Using Docker Only

If you use plain Docker (not Compose), you must pass the environment variable manually:

```bash
docker build -t weather-app .
docker run -d -p 8000:8000 \
  -e OPENWEATHER_API_KEY=your_api_key_here \
  weather-app
```

The app will be available at http://localhost:8000.