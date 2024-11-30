import google.generativeai as genai
import httpx
from httpx_socks import AsyncProxyTransport
from bot.config import GEMINI_API_KEY, PROXY_URL

class RhymeFinder:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY отсутствует. Проверьте файл .env.")

        # Настройка транспорта для использования SOCKS5-прокси
        self.transport = AsyncProxyTransport.from_url(PROXY_URL)

        # Создаем проксируемый HTTP-клиент
        self.client = httpx.AsyncClient(transport=self.transport)

        # Настройка API Gemini через кастомный HTTP-клиент
        genai.configure(api_key=GEMINI_API_KEY, http_client=self.client)

        # Инициализация модели Gemini
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def get_rhymes(self, word: str):
        try:
            # Формирование запроса
            prompt = f"Подбери рифмы для слова '{word}'. Ответ должен быть списком слов, разделённых запятыми, без лишнего текста. Не более 5 слов."
            response = self.model.generate_content(prompt)

            # Обработка ответа
            rhymes = response.text.strip().split(',')
            cleaned_rhymes = [rhyme.strip() for rhyme in rhymes if rhyme.strip()]
            return cleaned_rhymes
        except Exception as e:
            print(f"Ошибка при запросе к Gemini API: {e}")
            return []
        finally:
            await self.client.aclose()  # Закрытие клиента
