import argparse
import logging
import requests

logging.basicConfig(level=logging.INFO)


def main():
    parser = argparse.ArgumentParser(description="Weather CLI: Get current weather or forecast chart for a city (using API backend).")
    parser.add_argument("city", type=str, help="City name to look up weather for.")
    parser.add_argument("--forecast", action="store_true", help="Get 5-day/3-hour weather forecast chart instead of current weather chart.")
    parser.add_argument("--metric", type=str, default="temperature", choices=["temperature", "humidity", "wind_speed", "wind_deg"], help="Metric to plot (default: temperature)")
    parser.add_argument("--plot", action="store_true", help="Show the chart image (requires Pillow)")
    parser.add_argument("--api-base", type=str, default="http://127.0.0.1:5000", help="Base URL for the API (Flask or FastAPI)")
    args = parser.parse_args()

    endpoint = f"/chart/{args.city}/{args.metric}"
    url = args.api_base.rstrip("/") + endpoint
    try:
        resp = requests.get(url)
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return
    if resp.status_code == 200:
        chart_type = "forecast" if args.forecast else "current weather"
        print(f"{chart_type.title()} chart for {args.city} ({args.metric}):")
        if args.plot:
            try:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(resp.content))
                img.show()
            except ImportError:
                print("Pillow is not installed. Install it with 'pip install pillow' to display images.")
        else:
            print("Chart image received (use --plot to display)")
    else:
        print(f"Could not retrieve chart from API. Status: {resp.status_code}. Message: {resp.text}")

if __name__ == "__main__":
    main()
