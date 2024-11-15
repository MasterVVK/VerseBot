# bot/handlers/rhyme.py
from aiogram import Router, types
from bot.services.openai_service import get_rhymes_from_openai

router = Router()

@router.message()
async def find_rhyme(message: types.Message):
    word = message.text.strip()
    rhymes = await get_rhymes_from_openai(word)
    if rhymes:
        await message.answer(f"Рифмы для '{word}': {', '.join(rhymes)}")
    else:
        await message.answer("Не удалось найти рифмы, попробуйте позже.")
