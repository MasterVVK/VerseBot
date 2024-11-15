import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка на наличие необходимых токенов
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Отсутствуют необходимые токены. Проверьте файл .env.")
