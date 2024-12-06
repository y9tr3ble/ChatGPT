import asyncio
from aiogram import Bot

async def test_token(token: str):
    try:
        bot = Bot(token=token)
        me = await bot.get_me()
        print(f"Bot connection successful! Bot name: {me.full_name}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    token = "7482370857:AAEovxeVVjWfCrvz47P8_BJ6ZEQrWphse7I"
    asyncio.run(test_token(token)) 