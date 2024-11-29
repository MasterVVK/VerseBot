import aiohttp
import asyncio
from bot.config import YANDEX_API_KEY  # Импортируем только необходимую переменную


async def test_yandex_api():
    api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    if not YANDEX_API_KEY:
        raise ValueError("YANDEX_API_KEY отсутствует. Проверьте файл .env.")

    # Чтение текста из файлов
    try:
        with open("user_input.txt", "r", encoding="utf-8") as user_file:
            user_text = user_file.read().strip()
        with open("system_input.txt", "r", encoding="utf-8") as system_file:
            system_text = system_file.read().strip()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Не найден файл: {e.filename}. Убедитесь, что все файлы существуют.")

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": "gpt://b1g01ics4ffr66i0uv26/yandexgpt-32k/rc",
        "completionOptions": {
            "stream": False,
            "temperature": 0,
            "maxTokens": 10000
        },
        "messages": [
            {
                "role": "system",
                "text": system_text  # Используем текст из файла для system
            },
            {
                "role": "user",
                "text": user_text  # Используем текст из файла для user
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(api_url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    print("Ответ от API:")
                    print(result)
                else:
                    print(f"Ошибка: {response.status}, {await response.text()}")
        except Exception as e:
            print(f"Ошибка при запросе к Yandex API: {e}")


# Для выполнения теста используйте asyncio
if __name__ == "__main__":
    asyncio.run(test_yandex_api())
