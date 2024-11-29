import os
from httpx import AsyncClient
from httpx_socks import AsyncProxyTransport
from bot.config import ANTHROPIC_API_KEY, PROXY_URL

class RhymeFinder:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY отсутствует. Проверьте файл .env.")

        # Настройка транспорта для использования SOCKS5-прокси
        self.transport = AsyncProxyTransport.from_url(PROXY_URL)

        # Настройка HTTP-клиента через прокси
        self.client = AsyncClient(transport=self.transport, base_url="https://api.anthropic.com/v1")

    async def get_rhymes(self, word: str):
        headers = {
            "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": f"Ты помощник, который подбирает рифмы для слова '{word}'. Ответ должен быть списком слов, разделённых запятыми, без лишнего текста. Не более 5 слов.",
            "model": "claude-2",  # Проверьте актуальность модели
            "max_tokens_to_sample": 200,
            "temperature": 0.7
        }

        # Отладка
        print(f"URL запроса: {self.client.base_url}/completions")
        print(f"Payload: {payload}")

        try:
            response = await self.client.post("/completions", headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                rhymes = data.get("completion", "").strip().split(",")
                cleaned_rhymes = [rhyme.strip() for rhyme in rhymes if rhyme.strip()]
                return cleaned_rhymes
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return []
        except Exception as e:
            print(f"Ошибка при запросе к Anthropic API: {e}")
            return []
        finally:
            await self.client.aclose()  # Закрытие клиента
