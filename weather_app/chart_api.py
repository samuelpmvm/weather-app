from flask import Flask, request, jsonify, send_file
import io
import matplotlib.pyplot as plt
from weather_app.get_weather import get_weather_forecast

app = Flask(__name__)

@app.route('/chart/<city>/<metric>')
def chart(city, metric):
    """
    Endpoint to generate a chart for a given metric (temperature, humidity, wind_speed, wind_deg) for a city forecast.
    Example: /chart/Lisboa/temperature
    """
    result = get_weather_forecast(city)
    # Check metric validity first
    valid_metrics = {'temperature', 'humidity', 'wind_speed', 'wind_deg'}
    if metric not in valid_metrics:
        return jsonify({'error': 'Invalid metric'}), 400
    if not result or not result.get('forecasts'):
        return jsonify({'error': 'No forecast data found'}), 404
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
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
