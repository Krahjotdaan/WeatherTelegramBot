import json
import requests
from config import WEATHER_API_KEY


def get_location_keys(cities: list):
    location_keys = []

    for city in cities:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search?q={city}&apikey={WEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        location_keys.append(int(data[0]['Key']))

    return location_keys


def get_current_weather(location_keys: list):
    current_weather = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_weather.append(data)

    return current_weather


def get_1day_forecast(location_keys):
    day1_forecast = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        day1_forecast.append(data)

    return day1_forecast


def get_3days_forecast(location_keys):
    day3_forecast = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        day3_forecast.append(data[:3])

    return day3_forecast


def write_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
