import aiohttp
from bot.config import YANDEX_API_KEY  # Импортируем только необходимую переменную

class RhymeFinder:
    def __init__(self):
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        if not YANDEX_API_KEY:
            raise ValueError("YANDEX_API_KEY отсутствует. Проверьте файл .env.")

    async def get_rhymes(self, word: str):
        headers = {
            "Authorization": f"Api-Key {YANDEX_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "modelUri": "gpt://b1g01ics4ffr66i0uv26/yandexgpt/rc",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты помощник, который подбирает рифмы для слов. Твои ответы должны содержать только список слов, разделённых запятыми, без лишнего текста."
                },
                {
                    "role": "user",
                    "text": f"Подбери рифмы для слова '{word}'."
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        rhymes = result.get("result", {}).get("alternatives", [])[0].get("message", {}).get("text", "")
                        return rhymes.split(',')  # Предполагается, что рифмы разделены запятыми
                    else:
                        print(f"Ошибка: {response.status}, {await response.text()}")
                        return []
            except Exception as e:
                print(f"Ошибка при запросе к Yandex API: {e}")
                return []
