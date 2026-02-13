import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN_API')
TELEGRAM_ADMIN_ID = os.getenv('TELEGRAM_ADMIN')
OPENROUTER_KEY = os.getenv('OPENROUTER_API_KEY')
MITUP_KEY = os.getenv('MITUP_API_KEY')
MITU_URL = os.getenv('MITU_API_URL')