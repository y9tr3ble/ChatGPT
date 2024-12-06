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
        # Load environment variables from .env file
        env_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), '.env')
        if path.exists(env_path):
            load_dotenv(env_path)
        else:
            logging.warning("No .env file found")

        # Get required environment variables
        self.bot_token = environ.get('BOT_TOKEN')
        self.openai_api_key = environ.get('OPENAI_API_KEY')
        self.gemini_api_key = environ.get('GEMINI_API_KEY')

        # Check if required variables are set
        if not all([self.bot_token, self.openai_api_key, self.gemini_api_key]):
            missing = []
            if not self.bot_token:
                missing.append('BOT_TOKEN')
            if not self.openai_api_key:
                missing.append('OPENAI_API_KEY')
            if not self.gemini_api_key:
                missing.append('GEMINI_API_KEY')
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
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