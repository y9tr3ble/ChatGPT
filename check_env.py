import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

def check_env():
    # Get absolute path to .env
    env_path = os.path.abspath('.env')
    logging.info(f"Looking for .env at: {env_path}")
    
    # Check file existence
    if not os.path.exists(env_path):
        logging.error(f".env file not found at {env_path}")
        return
    
    # Load variables
    load_dotenv(env_path)
    
    # Check values
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    
    # Log details about each key
    logging.info(f"BOT_TOKEN length: {len(bot_token)}")
    if len(bot_token) > 10:
        logging.info(f"BOT_TOKEN starts with: {bot_token[:8]}...")
        logging.info(f"BOT_TOKEN ends with: ...{bot_token[-8:]}")
    else:
        logging.warning("BOT_TOKEN is too short or empty!")
        
    logging.info(f"OPENAI_API_KEY exists: {bool(openai_key)}")
    logging.info(f"GEMINI_API_KEY exists: {bool(gemini_key)}")

if __name__ == "__main__":
    check_env() 