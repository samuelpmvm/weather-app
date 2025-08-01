
# Weather App

This is a simple Python app that fetches weather data for a given location using the OpenWeatherMap API.

## Technologies Used

- Python 3
- requests (HTTP library)
- python-dotenv (environment variable management)
- OpenWeatherMap API
- GitHub Actions (for CI testing)

## Features

- Fetches current weather data for any city using OpenWeatherMap
- Secure API key management via `.env` file in `venv`
- Simple function interface for integration into other scripts
- Example usage and setup instructions
- Automated API test workflow with GitHub Actions

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install requests python-dotenv
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

Then, install the required package:
```bash
pip install python-dotenv
```

Your app will automatically load the API key from `venv/.env` when you run it.

Alternatively, you can set the environment variable manually:
```bash
export OPENWEATHER_API_KEY='your_api_key_here'
```
This can be added to your `.bashrc`, `.zshrc`, or run in your terminal before starting the app.

## Notes
- Make sure to keep your API key secure and never commit it to version control.
- The virtual environment directory (`venv`) is ignored by git (see `.gitignore`).