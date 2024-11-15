# bot/handlers/start.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я VerseBot, помогу найти рифмы для слов. Просто отправь мне слово, и я подберу рифмы.")
