from dataclasses import dataclass
from os import path, environ
from dotenv import load_dotenv, find_dotenv, dotenv_values
import logging
import re

@dataclass
class Config:
    bot_token: str
    openai_api_key: str
    gemini_api_key: str
    anthropic_api_key: str

    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        
        # Try to find .env file
        env_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), '.env')
        logging.info(f"Looking for .env at: {env_path}")
        
        # Also try to find .env using dotenv's built-in search
        alt_env_path = find_dotenv()
        if alt_env_path:
            logging.info(f"Alternative .env found at: {alt_env_path}")
        
        if path.exists(env_path):
            logging.info(f"Loading .env from: {env_path}")
            
            # Read values directly from .env file
            env_values = dotenv_values(env_path)
            logging.info("Direct values from .env file:")
            for key, value in env_values.items():
                masked_value = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
                logging.info(f"{key}={masked_value}")
            
            # Force set environment variables
            for key, value in env_values.items():
                environ[key] = value
                
            logging.info("Environment variables after setting:")
            if 'BOT_TOKEN' in environ:
                token = environ['BOT_TOKEN']
                masked_token = token[:4] + '...' + token[-4:] if len(token) > 8 else '***'
                logging.info(f"BOT_TOKEN={masked_token}")
        else:
            logging.error(f".env file not found at {env_path}")
            raise FileNotFoundError(f".env file not found at {env_path}")

        # Get and validate bot token
        self.bot_token = self._get_and_validate_token('BOT_TOKEN')
        self.openai_api_key = environ.get('OPENAI_API_KEY', '').strip()
        self.gemini_api_key = environ.get('GEMINI_API_KEY', '').strip()
        self.anthropic_api_key = environ.get('ANTHROPIC_API_KEY', '').strip()

    def _get_and_validate_token(self, env_var: str) -> str:
        """Get and validate bot token from environment variables"""
        # First check if variable exists
        if env_var not in environ:
            error_msg = f"{env_var} is not set in environment variables"
            logging.error(error_msg)
            logging.info(f"Available environment variables: {list(environ.keys())}")
            raise ValueError(error_msg)
            
        token = environ[env_var].strip()  # Use direct dictionary access
        
        # Log raw token for debugging
        logging.info(f"Raw {env_var} value: '{token}'")
        logging.info(f"Raw {env_var} length: {len(token)}")
        
        if not token:
            error_msg = f"{env_var} is empty"
            logging.error(error_msg)
            raise ValueError(error_msg)
        
        # Log token details for debugging
        if len(token) > 10:
            logging.info(f"{env_var} starts with: '{token[:8]}'")
            logging.info(f"{env_var} middle part: '{token[8:16]}'")
            logging.info(f"{env_var} ends with: '{token[-8:]}'")
            
            # Log character types for debugging
            logging.info("Token structure analysis:")
            parts = token.split(':')
            if len(parts) == 2:
                logging.info(f"ID part (before :): '{parts[0]}' (length: {len(parts[0])})")
                logging.info(f"Hash part (after :): '{parts[1]}' (length: {len(parts[1])})")
            else:
                logging.info(f"Token does not contain ':' separator. Parts found: {len(parts)}")
            
        # Validate token format (NUMBER:LETTERS)
        if not re.match(r'^\d+:[A-Za-z0-9_-]+$', token):
            error_msg = f"Invalid {env_var} format. Token should be in format: NUMBER:LETTERS"
            logging.error(error_msg)
            logging.error(f"Token format validation failed. Token contains invalid characters or format")
            raise ValueError(error_msg)
            
        return token