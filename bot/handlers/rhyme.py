# bot/handlers/rhyme.py
from aiogram import Router, types
from bot.services.openai_service import RhymeFinder

router = Router()
rhyme_finder = RhymeFinder()

@router.message()
async def find_rhyme(message: types.Message):
    word = message.text.strip()
    await message.answer("Ищу рифмы для вашего слова...")
    rhymes = await rhyme_finder.get_rhymes(word)
    if rhymes:
        await message.answer(f"Рифмы для '{word}': {', '.join(rhymes)}")
    else:
        await message.answer("Не удалось найти рифмы, попробуйте позже.")

