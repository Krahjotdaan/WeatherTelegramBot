import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from config import BOT_TOKEN
from weather_api import *
from formatting import *


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class Form(StatesGroup):
    """
    A class that defines the states of the checkpoints and type of api.
    """
    command = State()
    start_point = State()
    end_point = State()


@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    """
    Handles the /start command.

    Sends a welcome message to the user and explains the purpose of the bot.

    Args:
        message: The message object received from the user.
    """
    await message.reply("Привет! Я бот для прогноза погоды. Используй /help для получения помощи. Используй /weather для получения прогноза погоды")


@dp.message(F.text == '/help')
async def help_command(message: types.Message):
    """
    Handles the /help command.

    Sends a message with a description of available commands to the user.

    Args:
        message: The message object received from the user.
    """
    help_message = "Доступные команды:\n"
    help_message += "/start - приветствие и описание возможностей бота\n"
    help_message += "/help - список доступных команд и краткая инструкция\n"
    help_message += "/weather - запрос прогноза погоды (ввод начальной и конечной точки маршрута, временного интервала)"
    await message.reply(help_message)


@dp.message(F.text == '/weather')
async def weather_command(message: types.Message):
    """
    Handles the /weather command.

    Sends a message to the user with options to choose the type of weather forecast.

    Args:
        message: The message object received from the user.
    """
    weather_message = "Выбери опцию: \n"
    weather_message += "1. /current для получения текущей погоды \n"
    weather_message += "2. /1day для получения прогноза на следующий день \n"
    weather_message += "3. /3days для получения прогноза на 3 дня"
    await message.reply(weather_message)


@dp.message(Command(commands=["current"]))
async def current_weather(message: types.Message, state: FSMContext):
    """
    Handles the /current command.

    Starts the process of getting current weather by setting state to Form.start_point
    and prompting the user for start location.

    Args:
        message: The message object received from the user.
        state: The FSMContext object.
    """
    await state.update_data(command='current')
    await message.answer("Введите начальную точку на английском")
    await state.set_state(Form.start_point)


@dp.message(Command(commands=["1day"]))
async def day1_weather(message: types.Message, state: FSMContext):
    """
    Handles the /1day command.

    Starts the process of getting a 1-day forecast by setting state to Form.start_point
    and prompting the user for start location.

    Args:
        message: The message object received from the user.
        state: The FSMContext object.
    """
    await state.update_data(command='1day')
    await message.answer("Введите начальную точку на английском")
    await state.set_state(Form.start_point)


@dp.message(Command(commands=["3days"]))
async def days3_weather(message: types.Message, state: FSMContext):
    """
     Handles the /3days command.

    Starts the process of getting a 3-day forecast by setting state to Form.start_point
    and prompting the user for start location.

    Args:
        message: The message object received from the user.
        state: The FSMContext object.
    """
    await state.update_data(command='3days')
    await message.answer("Введите начальную точку на английском")
    await state.set_state(Form.start_point)


@dp.message(Form.start_point)
async def process_start_point(message: types.Message, state: FSMContext):
    """
    Handles the start point input from user in FSM

    Updates the state with start point and prompts user for end point

    Args:
        message: The message object received from the user.
        state: The FSMContext object.
    """
    await state.update_data(start_point=message.text)
    await message.answer("Введите конечную точку на английском")
    await state.set_state(Form.end_point)


@dp.message(Form.end_point)
async def process_end_point(message: types.Message, state: FSMContext):
    """
    Handles the end point input from user in FSM, retrieves weather data
    based on the selected command, formats it, and sends the result
    to the user.

    Args:
        message: The message object received from the user.
        state: The FSMContext object.
    """
    await state.update_data(end_point=message.text)

    api_type = await state.get_value('command')
    start_point = await state.get_value('start_point')
    end_point = await state.get_value('end_point')

    location_keys = get_location_keys([start_point, end_point])
    
    if api_type == 'current':
        data = get_current_weather(location_keys)
        main_params = get_current_main_params(data)
        strs = get_result_str(main_params)

        start_line = start_point + '\n' + strs[0]
        end_line = end_point + '\n' + strs[1]

        await message.answer(start_line)
        await message.answer(end_line)

    elif api_type == '1day':
        data = get_1day_forecast(location_keys)
        main_params = get_1day_forecast_main_params(data)
        strs = get_result_str(main_params)

        start_line = start_point + '\n' + strs[0]
        end_line = end_point + '\n' + strs[1]

        await message.answer(start_line)
        await message.answer(end_line)

    elif api_type == '3days':
        data = get_3days_forecast(location_keys)
        main_params = get_3days_forecast_main_params(data)
        strs = get_result_str(main_params)

        start_line = start_point + '\n' + '\n'.join(strs[:3])
        end_line = end_point + '\n' + '\n'.join(strs[:-3])

        await message.answer(start_line)
        await message.answer(end_line)

    await state.clear()


@dp.message()
async def handle_unrecognized_message(message: types.Message):
    """
    Handles unrecognized messages and sends a default response to the user.

    Args:
        message: The message object received from the user.
    """
    await message.answer('Извините, я не понял ваш запрос')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
