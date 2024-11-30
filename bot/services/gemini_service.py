import httpx
from httpx_socks import AsyncProxyTransport
from bot.config import GEMINI_API_KEY, PROXY_URL

class RhymeFinder:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY отсутствует. Проверьте файл .env.")

        # Настройка транспорта для использования SOCKS5-прокси
        self.transport = AsyncProxyTransport.from_url(PROXY_URL)
        # Создание асинхронного клиента с прокси
        self.client = httpx.AsyncClient(transport=self.transport)

        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    async def get_rhymes(self, word: str):
        params = {
            "key": GEMINI_API_KEY
        }
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "parts": [{"text": f"Подбери рифмы для слова '{word}'. Ответ должен быть списком слов, разделённых запятыми, без лишнего текста. Не более 5 слов."}]
            }]
        }

        try:
            # Выполнение асинхронного запроса с использованием API-ключа в параметре URL
            response = await self.client.post(self.base_url, headers=headers, params=params, json=payload)

            # Печать ответа для отладки
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")

            if response.status_code == 200:
                data = response.json()
                print(f"Parsed Response: {data}")  # Печатаем распарсенный ответ

                # Извлекаем текст рифм из правильного места
                candidates = data.get("candidates", [])
                if candidates:
                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if parts:
                        text = parts[0].get("text", "").strip()
                        if text:
                            # Разделяем текст на рифмы
                            rhymes = text.split(',')
                            cleaned_rhymes = [rhyme.strip() for rhyme in rhymes if rhyme.strip()]
                            return cleaned_rhymes
                        else:
                            print("Ошибка: Отсутствует поле 'text' в 'parts'.")
                            return []
                    else:
                        print("Ошибка: Отсутствует поле 'parts'.")
                        return []
                else:
                    print("Ошибка: Отсутствуют кандидаты в ответе.")
                    return []
            else:
                print(f"Ошибка при запросе: {response.status_code}, {response.text}")
                return []
        except Exception as e:
            print(f"Ошибка при запросе к Gemini API: {e}")
            return []
        finally:
            await self.client.aclose()  # Закрытие клиента
