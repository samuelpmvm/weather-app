import argparse
import logging
import requests

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Weather CLI: Get current weather or forecast for a city.")
    parser.add_argument("city", type=str, help="City name to look up weather for.")
    parser.add_argument("--forecast", action="store_true", help="Get 5-day/3-hour weather forecast instead of current weather.")
    parser.add_argument("--plot", action="store_true", help="Show a chart of temperature forecast (requires --forecast)")
    args = parser.parse_args()

    api_base = "http://127.0.0.1:5000"
    if args.forecast:
        resp = requests.get(f"{api_base}/chart/{args.city}/temperature")
        if resp.status_code == 200:
            print(f"Weather forecast chart for {args.city} (temperature):")
            if args.plot:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(resp.content))
                img.show()
            else:
                print("Chart image received (use --plot to display)")
        else:
            print("Could not retrieve forecast chart from API.")
    else:
        resp = requests.get(f"{api_base}/chart/{args.city}/temperature")
        if resp.status_code == 200:
            print(f"Current weather chart for {args.city} (temperature):")
            if args.plot:
                from PIL import Image
                import io
                img = Image.open(io.BytesIO(resp.content))
                img.show()
            else:
                print("Chart image received (use --plot to display)")
        else:
            print("Could not retrieve weather chart from API.")

if __name__ == "__main__":
    main()
