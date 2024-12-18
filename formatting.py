def get_current_main_params(data: list):
    main_params_list = []

    for d in data:
        main_params = {}

        main_params["date"] = "Текущая погода"
        main_params["temp"] = d["Temperature"]["Metric"]["Value"]
        main_params["weather_text"] = d["WeatherText"]
        main_params["precipitation"] = d["HasPrecipitation"]
        main_params["humidity"] = d["RelativeHumidity"]
        main_params["wind_speed"] = round(d["Wind"]["Speed"]["Metric"]["Value"] * 1000 / 3600, 1) # переводит скорость ветра в м/с

        main_params_list.append(main_params)

    return main_params_list


def get_forecast_main_params(data: list):
    main_params_list = []

    for d in data:
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


def get_result_str(main_params_list: list):
    results = []

    for data in main_params_list:
        result_str = ""

        result_str += str(data["date"]) + '\n'
        result_str += f'Температура: {data["temp"]}C \n'
        result_str += f'Погода: {data["weather_text"]} \n'
        result_str += f'Осадки: {data["precipitation"]} \n'
        result_str += f'Относительная влажность: {data["humidity"]}% \n'
        result_str += f'Скорость ветра: {data["wind_speed"]} м/c \n'

        results.append(result_str)

    return results
