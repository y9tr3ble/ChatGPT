import asyncio
import logging
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramAPIError
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from src.config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

async def test_bot():
    session = None
    try:
        # Load config
        config = Config()
        token = config.bot_token.strip()
        
        # Log token details (length and first/last few chars)
        logging.info(f"Raw token length: {len(token)}")
        if len(token) > 10:
            logging.info(f"Token starts with: '{token[:8]}'")
            logging.info(f"Token ends with: '{token[-8:]}'")
        
        # Initialize bot with session
        session = AiohttpSession()
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token=token, session=session, default=default)
        
        # Test connection
        bot_info = await bot.get_me()
        logging.info(f"Successfully connected to bot: {bot_info.full_name}")
        logging.info(f"Bot username: @{bot_info.username}")
        logging.info(f"Bot ID: {bot_info.id}")
        
    except Exception as e:
        if isinstance(e, TelegramAPIError):
            logging.error(f"Telegram API Error: {str(e)}")
        else:
            logging.error(f"Error: {str(e)}")
        raise
    finally:
        if session is not None:
            await session.close()

def main():
    try:
        asyncio.run(test_bot())
    except KeyboardInterrupt:
        logging.info("Test cancelled by user")
    except Exception as e:
        logging.error(f"Test failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main() 