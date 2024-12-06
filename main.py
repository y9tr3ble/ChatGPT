import asyncio
import logging
import sys
from os import path

# Добавляем корневую директорию проекта в sys.path
project_root = path.dirname(path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from src.config import Config
from src.bot.handlers import common, language, chat
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
from src.bot.middlewares.language import LanguageMiddleware

async def main():
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    try:
        # Load config and print token (временно для отладки)
        config = Config()
        logging.info(f"Token length: {len(config.bot_token)}")
        
        # Initialize bot and test connection
        default = DefaultBotProperties(parse_mode=ParseMode.HTML)
        bot = Bot(token=config.bot_token, default=default)
        bot_info = await bot.get_me()
        logging.info(f"Bot connection successful! Bot name: {bot_info.full_name}")
        
        # Initialize services
        message_service = MessageService()
        openai_service = OpenAIService(config.openai_api_key)
        
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
        
        # Start polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"Startup error: {e}")
        raise
    finally:
        if 'bot' in locals():
            await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
