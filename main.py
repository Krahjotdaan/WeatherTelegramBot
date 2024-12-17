from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import logging
import asyncio
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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


@dp.message()
async def handle_unrecognized_message(message: types.Message):
    await message.answer('Извините, я не понял ваш запрос. Попробуйте использовать команды или кнопки.')


if __name__ == '__main__':
    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())