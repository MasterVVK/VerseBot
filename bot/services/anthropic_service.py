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
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",  # Убедитесь, что модель доступна
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": f"Подбери рифмы для слова '{word}'. Ответ должен быть списком слов, разделённых запятыми, без лишнего текста. Не более 5 слов."
                }
            ]
        }

        try:
            # Отправка запроса к Anthropic API
            response = await self.client.post("/messages", headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                # Извлечение текста из поля content
                content_list = data.get("content", [])
                if content_list and content_list[0].get("type") == "text":
                    rhymes = content_list[0].get("text", "").strip().split(",")
                    cleaned_rhymes = [rhyme.strip() for rhyme in rhymes if rhyme.strip()]
                    return cleaned_rhymes
                else:
                    print("Ошибка: Неверный формат ответа.")
                    return []
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return []
        except Exception as e:
            print(f"Ошибка при запросе к Anthropic API: {e}")
            return []
        finally:
            await self.client.aclose()  # Закрытие клиента
