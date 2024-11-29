# bot/handlers/rhyme.py
from aiogram import Router, types
from bot.services.openai_service import RhymeFinder as OpenAIRhymeFinder
from bot.services.yandex_service import RhymeFinder as YandexRhymeFinder
from bot.services.gigachat_service import RhymeFinder as GigaChatRhymeFinder
from bot.services.anthropic_service import RhymeFinder as AnthropicRhymeFinder

router = Router()

openai_finder = OpenAIRhymeFinder()
yandex_finder = YandexRhymeFinder()
gigachat_finder = GigaChatRhymeFinder()
anthropic_finder = AnthropicRhymeFinder()

@router.message()
async def find_rhyme(message: types.Message):
    word = message.text.strip()

    # Проверка на одно слово
    if len(word.split()) > 1:
        await message.answer("Пожалуйста, отправьте только одно слово для подбора рифм.")
        return

    await message.answer("Ищу рифмы для вашего слова...")

    # Асинхронный вызов всех сервисов
    openai_rhymes = await openai_finder.get_rhymes(word)
    yandex_rhymes = await yandex_finder.get_rhymes(word)
    gigachat_rhymes = await gigachat_finder.get_rhymes(word)
    anthropic_rhymes = await anthropic_finder.get_rhymes(word)

    # Формирование ответа
    response = "Результаты:\n"
    #response += f"ChatGPT gpt-4o: {', '.join(openai_rhymes) if openai_rhymes else 'Не удалось найти рифмы'}\n"
    #response += f"YandexGPT 4 Pro RC: {', '.join(yandex_rhymes) if yandex_rhymes else 'Не удалось найти рифмы'}\n"
    #response += f"GigaChat-Pro: {', '.join(gigachat_rhymes) if gigachat_rhymes else 'Не удалось найти рифмы'}\n"
    response += f"Anthropic Claude: {', '.join(anthropic_rhymes) if anthropic_rhymes else 'Не удалось найти рифмы'}"

    await message.answer(response)
