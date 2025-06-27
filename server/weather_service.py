import requests
from config import OPENWEATHER_API_KEY, BASE_URL, FORECAST_URL
import cache


def normalize_input(value):
    return value.strip().lower()


def build_url(query_type, value):
    if query_type == "city":
        return f"{BASE_URL}?q={value},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    elif query_type == "pincode":
        return f"{BASE_URL}?zip={value},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    return None


def build_forecast_url(query_type, value):
    if query_type == "city":
        return f"{FORECAST_URL}?q={value},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    elif query_type == "pincode":
        return f"{FORECAST_URL}?zip={value},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    return None


def get_weather(query_type, value):
    key = f"{query_type}:{normalize_input(value)}"

    cached = cache.get(key)

    if cached is not None:
        return cached

    try:
        url = build_url(query_type, value)
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()

        forecast_url = build_forecast_url(query_type, value)
        forecast_resp = requests.get(forecast_url)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()

        tomorrow = forecast_data["list"][8]

        result = {
            "location": data["name"],
            "current": {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            },
            "forecast": {
                "temperature": tomorrow["main"]["temp"],
                "description": tomorrow["weather"][0]["description"],
            }
        }

        cache.set(key, result)
        return result
    except requests.RequestException as e:
        return {"error": str(e)}
    except (KeyError, IndexError) as e:
        return {"error": "Could not parse forecast data"}