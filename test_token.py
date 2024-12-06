import asyncio
from aiogram import Bot
import logging

logging.basicConfig(level=logging.INFO)

async def test_bot():
    token = "7482370857:AAEovxeVVjWfCrvz47P8_BJ6ZEQrWphse7I"
    try:
        bot = Bot(token=token)
        bot_info = await bot.get_me()
        logging.info(f"Successfully connected to bot: {bot_info.full_name}")
        await bot.session.close()
    except Exception as e:
        logging.error(f"Failed to connect: {e}")

if __name__ == "__main__":
    asyncio.run(test_bot()) 