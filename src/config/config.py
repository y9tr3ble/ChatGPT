from dataclasses import dataclass
from os import getenv, path, environ
from dotenv import load_dotenv
import logging
import sys

@dataclass
class Config:
    bot_token: str
    openai_api_key: str
    gemini_api_key: str

    def __init__(self):
        # Очищаем существующие переменные окружения
        if "BOT_TOKEN" in environ:
            del environ["BOT_TOKEN"]
        if "OPENAI_API_KEY" in environ:
            del environ["OPENAI_API_KEY"]
        if "GEMINI_API_KEY" in environ:
            del environ["GEMINI_API_KEY"]
            
        # Определяем путь к корневой директории проекта
        project_root = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
        env_path = path.join(project_root, '.env')
        
        # Проверяем наличие файла .env
        if not path.exists(env_path):
            raise FileNotFoundError(f".env file not found at {env_path}")
        
        # Загружаем переменные окружения
        load_dotenv(env_path, override=True)
        
        # Читаем файл напрямую для отладки
        with open(env_path, 'r') as f:
            env_content = f.read()
            logging.info(f"Raw .env content:\n{env_content}")
        
        # Получаем значения
        self.bot_token = getenv("BOT_TOKEN")
        self.openai_api_key = getenv("OPENAI_API_KEY")
        self.gemini_api_key = getenv("GEMINI_API_KEY")
        
        # Отладочная информация
        logging.info(f"Project root: {project_root}")
        logging.info(f"Loading .env from: {env_path}")
        logging.info(f"BOT_TOKEN length: {len(self.bot_token) if self.bot_token else 0}")
        logging.info(f"First 10 chars of BOT_TOKEN: {self.bot_token[:10] if self.bot_token else 'None'}")
        
        self._validate_config()
        
    def _validate_config(self) -> None:
        """Validate that all required environment variables are set"""
        if not self.bot_token:
            raise ValueError("BOT_TOKEN environment variable is not set")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
            
        if len(self.bot_token) < 30:  # Минимальная длина валидного токена
            raise ValueError(f"BOT_TOKEN seems too short: {len(self.bot_token)} chars")
            
        logging.info("Configuration loaded successfully") 