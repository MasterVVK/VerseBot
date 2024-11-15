from openai import OpenAI
import os
from bot.config import OPENAI_API_KEY, PROXY_URL

os.environ["http_proxy"] = PROXY_URL
os.environ["https_proxy"] = PROXY_URL

class RhymeFinder:
    def __init__(self):
        # Установка ключа API
        openai_key = OPENAI_API_KEY
        # Настройка прокси
        self.client = OpenAI(api_key=openai_key)

    async def get_rhymes(self, word: str):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты помощник, который подбирает рифмы для слов. Твои ответы должны содержать только список слов, разделённых запятыми, без лишнего текста."},
                {"role": "user", "content": f"Подбери рифмы для слова '{word}'."}
            ]
        )
        return response.choices[0].message.content.strip().split(',')
