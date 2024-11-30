# bot/main.py
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from bot.handlers import start, rhyme
import asyncio
from config import TELEGRAM_BOT_TOKEN

# Создание объекта DefaultBotProperties для настройки parse_mode
#bot_properties = DefaultBotProperties(parse_mode="MarkdownV2")

# Создание экземпляра бота с настройками по умолчанию
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Регистрация обработчиков
dp.include_router(start.router)
dp.include_router(rhyme.router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
