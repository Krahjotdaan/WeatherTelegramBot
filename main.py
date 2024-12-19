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
    command = State()
    start_point = State()
    end_point = State()


@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для прогноза погоды. Используй /help для получения помощи. Используй /weather для получения прогноза погоды")


@dp.message(F.text == '/help')
async def help_command(message: types.Message):
    help_message = "Доступные команды:\n"
    help_message += "/start - приветствие и описание возможностей бота\n"
    help_message += "/help - список доступных команд и краткая инструкция\n"
    help_message += "/weather - запрос прогноза погоды (ввод начальной и конечной точки маршрута, временного интервала)"
    await message.reply(help_message)


@dp.message(F.text == '/weather')
async def weather_command(message: types.Message):
    weather_message = "Выбери опцию: \n"
    weather_message += "1. /current для получения текущей погоды \n"
    weather_message += "2. /1day для получения прогноза на следующий день \n"
    weather_message += "3. /3days для получения прогноза на 3 дня"
    await message.reply(weather_message)


@dp.message(Command(commands=["current"]))
async def current_weather(message: types.Message, state: FSMContext):
    await state.update_data(command='current')
    await message.answer("Введите начальную точку")
    await state.set_state(Form.start_point)


@dp.message(Command(commands=["1day"]))
async def day1_weather(message: types.Message, state: FSMContext):
    await state.update_data(command='current')
    await message.answer("Введите начальную точку")
    await state.set_state(Form.start_point)


@dp.message(Command(commands=["3days"]))
async def days3_weather(message: types.Message, state: FSMContext):
    await state.update_data(command='current')
    await message.answer("Введите начальную точку")
    await state.set_state(Form.start_point)


@dp.message(Form.start_point)
async def process_start_point(message: types.Message, state: FSMContext):
    await state.update_data(start_point=message.text)
    await message.answer("Введите конечную точку")
    await state.set_state(Form.end_point)


@dp.message(Form.end_point)
async def process_end_point(message: types.Message, state: FSMContext):
    await state.update_data(end_point=message.text)
    s = await state.get_data()
    await message.answer(', '.join([s.get('start_point'), s.get('end_point')]))
    await state.clear()


@dp.message(F.text != '/current' and F.text != '/1day' and F.text != '/3days')
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
