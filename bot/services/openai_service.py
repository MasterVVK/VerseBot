import os
import asyncio
from openai import AsyncOpenAI
from httpx import AsyncClient
from httpx_socks import AsyncProxyTransport
from bot.config import OPENAI_API_KEY, PROXY_URL


class RhymeFinder:
    def __init__(self):
        # Настройка транспорта для использования SOCKS5-прокси
        self.transport = AsyncProxyTransport.from_url(PROXY_URL)
        # Настройка HTTP-клиента через прокси
        self.client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            http_client=AsyncClient(transport=self.transport)
        )

    async def get_rhymes(self, word: str):
        # Выполнение асинхронного запроса через OpenAI API
        response = await self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "Ты помощник, который подбирает рифмы для слов. Твои ответы должны содержать только список слов, разделённых запятыми, без лишнего текста. Не более 5 слов."},
                {"role": "user", "content": f"Подбери рифмы для слова '{word}'."}
            ]
        )
        return response.choices[0].message.content.strip().split(',')
