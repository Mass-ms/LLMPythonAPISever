import json
import os
from http import HTTPStatus

import requests

owm_api_key = os.environ["TOKEN_OPENWEATHERMAP"]


def get_current_weather(region: str, unit: str = "celsius") -> json:
    data = fetch_weather_api(region)
    weather_info = {
        "region": data["name"],
        "temperature": data["main"]["temp"],
        "unit": unit,
        "forecast": data["weather"][0]["description"],
    }
    return json.dumps(weather_info)


def fetch_weather_api(region: str):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={region}&appid={owm_api_key}&lang=ja&units=metric",
    )
    if response.status_code == HTTPStatus.OK:
        data = response.json()
    return data


if __name__ == "__main__":
    print(get_current_weather("Nagoya,JP"))
