import json
import requests
from config import WEATHER_API_KEY


def get_location_key(city):
    """
    Retrieves the location key from AccuWeather API using city name.

    Args:
        city: name of the city

    Returns:
        The location key.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """

    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?q={city}&apikey={WEATHER_API_KEY}"
    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    return data[0]['Key']


def get_current_weather_data(location_key):
    """
    Retrieves current weather data from AccuWeather API using a location key.

    Args:
        location_key: The location key obtained from get_location_key().

    Returns:
        A dictionary containing the weather data.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    
    url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={WEATHER_API_KEY}&details=true"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return data


def get_main_params(data: dict):
    """
    Extracts and formats key weather parameters from a dictionary.

    Args:
        data: A dictionary containing raw weather data.  Assumed to have keys 
              like "Temperature", "RealFeelTemperature", "WeatherText", etc.

    Returns:
        A dictionary containing formatted weather parameters: temp, feel_temp, 
        weather_text, precipitation, humidity, wind_speed, direction, pressure.
    """

    main_params = {}

    main_params["temp"] = data["Temperature"]["Metric"]["Value"]
    main_params["feel_temp"] = data["RealFeelTemperature"]["Metric"]["Value"]
    main_params["weather_text"] = data["WeatherText"]
    main_params["precipitation"] = data["HasPrecipitation"]
    main_params["humidity"] = data["RelativeHumidity"]
    main_params["wind_speed"] = round(data["Wind"]["Speed"]["Metric"]["Value"] * 1000 / 3600, 1)
    main_params["direction"] = data["Wind"]["Direction"]["English"]
    main_params["pressure"] = round(data["Pressure"]["Metric"]["Value"] * 100 * 0.007501, 0)

    return main_params


def get_result_str(main_params: dict):
    """
    Generates a formatted string summarizing weather conditions.

    Args:
        main_params: A dictionary containing formatted weather parameters 
                     (output from get_main_params).

    Returns:
        A formatted string describing the weather, including an assessment of 
        whether conditions are favorable or unfavorable.
    """
    
    result_str = ""

    result_str += f'Температура: {main_params["temp"]}C \n'
    result_str += f'Ощущается как: {main_params["feel_temp"]}C \n'
    result_str += f'Погода: {main_params["weather_text"]} \n'
    result_str += f'Осадки: {main_params["precipitation"]} \n'
    result_str += f'Относительная влажность: {main_params["humidity"]}% \n'
    result_str += f'Скорость ветра: {main_params["wind_speed"]} м/c \n'
    result_str += f'Направление ветра: {main_params["direction"]} \n'
    result_str += f'Давление: {main_params["pressure"]} мм.рт.ст \n'


def write_to_file(data):
    with open('1.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)
