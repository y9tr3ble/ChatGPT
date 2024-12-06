import asyncio
import logging
import sys
from os import path

# Add project root to sys.path
project_root = path.dirname(path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramAPIError
from aiogram.client.default import DefaultBotProperties

from src.config import Config
from src.bot.handlers import common, language, chat
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
from src.services.gemini_service import GeminiService
from src.services.gpt4o_service import GPT4OService
from src.services.claude_service import ClaudeService
from src.services.user_service import UserService
from src.bot.middlewares.language import LanguageMiddleware
from src.services.storage_service import StorageService

async def create_bot(token: str) -> Bot:
    """Create and validate bot instance"""
    session = AiohttpSession()
    default = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=token, session=session, default=default)
    
    try:
        # Test bot token by getting bot info
        bot_info = await bot.get_me()
        logging.info(f"Successfully initialized bot: {bot_info.full_name}")
        return bot
    except TelegramAPIError as e:
        await session.close()
        error_msg = f"Failed to initialize bot: {str(e)}"
        logging.error(error_msg)
        raise ValueError(error_msg)

async def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    bot = None
    try:
        # Load config
        config = Config()
        
        # Initialize bot
        bot = await create_bot(config.bot_token)
        
        # Initialize services
        storage_service = StorageService()
        message_service = MessageService(storage_service)
        openai_service = OpenAIService(config.openai_api_key)
        gemini_service = GeminiService(config.gemini_api_key)
        gpt4o_service = GPT4OService(config.openai_api_key)
        claude_service = ClaudeService(config.anthropic_api_key)
        user_service = UserService(storage_service)
        
        # Clear all messages at startup
        message_service.clear_all_messages()
        logging.info("All message histories cleared")
        
        # Initialize dispatcher
        dp = Dispatcher(storage=MemoryStorage())
        
        # Register middlewares
        dp.message.middleware(LanguageMiddleware(message_service))
        
        # Register routers
        dp.include_router(language.router)
        dp.include_router(common.router)
        dp.include_router(chat.router)
        
        # Set up services for handlers
        dp["message_service"] = message_service
        dp["openai_service"] = openai_service
        dp["gemini_service"] = gemini_service
        dp["gpt4o_service"] = gpt4o_service
        dp["claude_service"] = claude_service
        dp["user_service"] = user_service
        
        # Start polling
        logging.info("Starting bot...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"Startup error: {str(e)}")
        raise
    finally:
        if bot is not None:
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
