import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
checkpoints = []


@dp.message(F.text == '/start')
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот для прогноза погоды. Используй /help для получения помощи. Используй /weather для получения прогноза погоды")


@dp.message(F.text == '/help')
async def help_command(message: types.Message):
    help_message = "Доступные команды:\n"
    help_message += "/start - приветствие и описание возможностей бота\n"
    help_message += "/help - список доступных команд и краткая инструкция\n"
    help_message += "/weather - запрос прогноза погоды (ввод начальной и конечной точки маршрута, временного интервала и промежуточных остановок)"
    await message.reply(help_message)


@dp.message(F.text == '/weather')
async def weather_command(message: types.Message):
    weather_message = "Выбери опцию: \n"
    weather_message += "1. /current для получения текущей погоды \n"
    weather_message += "2. /1day для получения прогноза на следующий день \n"
    weather_message += "3. /5days для получения прогноза на 5 дней"
    await message.reply(weather_message)


@dp.message(F.text == '/current')
async def current_weather(message: types.Message):
    await message.reply('fisting')


@dp.message(F.text == '/1day')
async def day1_weather(message: types.Message):
    await message.reply('spanking')


@dp.message(F.text == '/5days')
async def days5_weather(message: types.Message):
    await message.reply('suction')

    
@dp.message()
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды.')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
