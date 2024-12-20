import json
import requests
from config import WEATHER_API_KEY


def get_location_keys(cities: list):
    """
    Retrieves location keys for a list of cities using the AccuWeather API.

    Args:
        cities: A list of city names as strings.

    Returns:
        A list of location keys (integers) corresponding to the provided cities.
        Returns an empty list if no keys were found for the given cities.

    Raises:
        requests.exceptions.HTTPError: If the API request returns an error.
    """
    location_keys = []

    for city in cities:
        url = f"http://dataservice.accuweather.com/locations/v1/cities/search?q={city}&apikey={WEATHER_API_KEY}"
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()

        location_keys.append(int(data[0]['Key']))

    return location_keys


def get_current_weather(location_keys: list):
    """
    Retrieves current weather conditions for a list of location keys.

    Args:
        location_keys: A list of location keys (integers).

    Returns:
         A list of lists of dictionaries, where each inner list contains a single dictionary
         representing the current weather conditions for the corresponding location key.
    
    Raises:
        requests.exceptions.HTTPError: If the API request returns an error.
    """
    current_weather = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current_weather.append(data)

    return current_weather


def get_1day_forecast(location_keys):
    """
    Retrieves a 1-day weather forecast for a list of location keys.

    Args:
        location_keys: A list of location keys (integers).

    Returns:
        A list of dictionaries, where each dictionary contains the 1-day forecast
        data for the corresponding location key.

    Raises:
        requests.exceptions.HTTPError: If the API request returns an error.
    """
    day1_forecast = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        day1_forecast.append(data)

    return day1_forecast


def get_3days_forecast(location_keys):
    """
    Retrieves a 5-day weather forecast for a list of location keys.
    Only the first 3 days are used.

    Args:
        location_keys: A list of location keys (integers).

    Returns:
        A list of dictionaries, where each dictionary contains the 5-day forecast
        data for the corresponding location key.

    Raises:
        requests.exceptions.HTTPError: If the API request returns an error.
    """
    day3_forecast = []

    for location_key in location_keys:
        url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={WEATHER_API_KEY}&details=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        day3_forecast.append(data)

    return day3_forecast


def write_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
