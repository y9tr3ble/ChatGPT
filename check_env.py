import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

def check_env():
    # Получаем абсолютный путь к .env
    env_path = os.path.abspath('.env')
    logging.info(f"Looking for .env at: {env_path}")
    
    # Проверяем существование файла
    if not os.path.exists(env_path):
        logging.error(f".env file not found at {env_path}")
        return
    
    # Загружаем переменные
    load_dotenv(env_path)
    
    # Проверяем значения
    bot_token = os.getenv("BOT_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    logging.info(f"BOT_TOKEN: '{bot_token}'")
    logging.info(f"BOT_TOKEN length: {len(bot_token) if bot_token else 0}")
    logging.info(f"OPENAI_API_KEY exists: {bool(openai_key)}")

if __name__ == "__main__":
    check_env() 