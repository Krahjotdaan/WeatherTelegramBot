def get_current_main_params(data: list):
    """
    Extracts and processes key weather parameters from current conditions data.

    Args:
        data: A list of lists, where each inner list contains a single dictionary
              representing current weather conditions.

    Returns:
        A list of dictionaries, each containing formatted weather parameters
        such as date, temperature, weather description, precipitation status,
        humidity, and wind speed.
    """
    main_params_list = []

    for item in data:
        main_params = {}
        d = item[0]

        main_params["date"] = "Текущая погода"
        main_params["temp"] = d["Temperature"]["Metric"]["Value"]
        main_params["weather_text"] = d["WeatherText"]
        main_params["precipitation"] = d["HasPrecipitation"]
        main_params["humidity"] = d["RelativeHumidity"]
        main_params["wind_speed"] = round(d["Wind"]["Speed"]["Metric"]["Value"] * 1000 / 3600, 1) # переводит скорость ветра в м/с

        main_params_list.append(main_params)

    return main_params_list


def get_1day_forecast_main_params(data: list):
    """
    Extracts and processes key weather parameters from a 1-day forecast data.

    Args:
        data: A list of dictionaries, where each dictionary contains a key
              'DailyForecasts' which is a list of daily forecast data.

    Returns:
        A list of dictionaries, each containing formatted weather parameters
        for the first day in the forecast, such as date, temperature, weather
        description, precipitation type, humidity, and wind speed.
    """
    main_params_list = []

    for item in data:
        d = item['DailyForecasts'][0]
        main_params = {}

        main_params["date"] = d["Date"]

        min_temp = d["Temperature"]["Minimum"]["Value"]
        max_temp = d["Temperature"]["Maximum"]["Value"]

        min_temp = (min_temp - 32) / 1.8 # перевод из шкалы Фаренгейта в Цельсия
        max_temp = (max_temp - 32) / 1.8
        temp = (min_temp + max_temp) / 2

        main_params["temp"] = round(temp, 0)
        main_params["weather_text"] = d["Day"]["ShortPhrase"]
        main_params["precipitation"] = d["Day"]["PrecipitationType"]
        main_params["humidity"] = d["Day"]["RelativeHumidity"]["Average"]
        main_params["wind_speed"] = round(d["Day"]["Wind"]["Speed"]["Value"] * 0.446944, 1) # перевод скорости ветра из миль в час в м/с

        main_params_list.append(main_params)

    return main_params_list
    

def get_3days_forecast_main_params(data: list):
    """
    Extracts and processes key weather parameters from a 3-day forecast data.

    Args:
        data: A list of dictionaries, where each dictionary contains a key
              'DailyForecasts' which is a list of daily forecast data.

    Returns:
        A list of dictionaries, each containing formatted weather parameters
        for the first three days in the forecast, such as date, temperature,
        weather description, precipitation type, humidity, and wind speed.
    """
    main_params_list = []

    for item in data:
        for d in item["DailyForecasts"][:3]:
            main_params = {}

            main_params["date"] = d["Date"]

            min_temp = d["Temperature"]["Minimum"]["Value"]
            max_temp = d["Temperature"]["Maximum"]["Value"]

            min_temp = (min_temp - 32) / 1.8 # перевод из шкалы Фаренгейта в Цельсия
            max_temp = (max_temp - 32) / 1.8
            temp = (min_temp + max_temp) / 2

            main_params["temp"] = round(temp, 0)
            main_params["weather_text"] = d["Day"]["ShortPhrase"]
            if d["Day"]["HasPrecipitation"]:
                main_params["precipitation"] = d["Day"]["PrecipitationType"]
            else:
                main_params["precipitation"] = "Отсутствуют"
            main_params["humidity"] = d["Day"]["RelativeHumidity"]["Average"]
            main_params["wind_speed"] = round(d["Day"]["Wind"]["Speed"]["Value"] * 0.446944, 1) # перевод скорости ветра из миль в час в м/с

            main_params_list.append(main_params)

    return main_params_list


def get_result_str(main_params_list: list):
    """
     Formats a list of weather parameters dictionaries into a list of strings.

    Args:
        main_params_list: A list of dictionaries, where each dictionary contains
                         formatted weather parameters (e.g., date, temperature,
                         weather description, precipitation, humidity, and
                         wind speed).

    Returns:
        A list of strings, where each string represents formatted weather data.
    """
    results = []

    for data in main_params_list:
        result_str = ""

        result_str += data["date"].split('T')[0] + '\n'
        result_str += f'Температура: {data["temp"]}C \n'
        result_str += f'Погода: {data["weather_text"]} \n'
        result_str += f'Осадки: {data["precipitation"]} \n'
        result_str += f'Относительная влажность: {data["humidity"]}% \n'
        result_str += f'Скорость ветра: {data["wind_speed"]} м/c \n'

        results.append(result_str)

    return results
