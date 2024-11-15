from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from bot.config import GIGACHAT_API_KEY  # Убедитесь, что ключ API загружается в config.py

class RhymeFinder:
    def __init__(self):
        if not GIGACHAT_API_KEY:
            raise ValueError("GIGACHAT_API_KEY отсутствует. Проверьте файл .env.")

        # Настройка клиента GigaChat
        self.llm = GigaChat(
            credentials=GIGACHAT_API_KEY,
            scope="GIGACHAT_API_PERS",
            model="GigaChat-Pro",
            verify_ssl_certs=False,
            streaming=False
        )

    async def get_rhymes(self, word: str):
        messages = [
            SystemMessage(
                content="Ты помощник, который подбирает рифмы для слов. Ответы должны содержать только список слов, разделенных запятыми. Не более 5 слов"
            ),
            HumanMessage(content=f"Подбери рифмы для слова '{word}'.")
        ]

        try:
            # Выполнение запроса
            res = self.llm.invoke(messages)
            rhymes = res.content.strip().split(',')
            cleaned_rhymes = [rhyme.strip() for rhyme in rhymes if rhyme.strip()]
            return cleaned_rhymes
        except Exception as e:
            print(f"Ошибка при запросе к GigaChat API: {e}")
            return []
