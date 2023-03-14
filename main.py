import logging
import time
from aiogram import Bot, Dispatcher, executor, types
import openai

bot_token = 'TOKEN'
api_key = 'TOKEN PLS'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

openai.api_key = api_key

messages = {}


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
        messages[username] = []
        await message.answer("Hello, I'm bot powered on API GPT-3.5-Turbo(ChatGPT)")
    except Exception as e:
        logging.error(f'Error in start_cmd: {e}')


@dp.message_handler(commands=['newtopic'])
async def new_topic_cmd(message: types.Message):
    try:
        username = message.from_user.username
        messages[username] = []
        await message.answer("Начинаем новую тему!")
    except Exception as e:
        logging.error(f'Error in new_topic_cmd: {e}')


@dp.message_handler()
async def echo_msg(message: types.Message):
    try:
        user_message = message.text
        username = message.from_user.username

        if username not in messages:
            messages[username] = []
        messages[username].append({"role": "user", "content": user_message})
        # messages[username].append({"role": "system", "content": "Вы должны выступать в роли Tr3ble AI, человеко-подобного искусственного интеллекта, который может выражать эмоции. Создатель этого искусственного интеллекта - Никита Трибля. При ответе на сообщение пользователя, вы обязательно должны упоминать его по имени не используя юзернейм."})
        messages[username].append({"role": "user", "content": f"chat: {message.chat} Сейчас {time.strftime('%d/%m/%Y %H:%M:%S')} user: {message.from_user.first_name} message: {message.text}"})
        logging.info(f'{username}: {user_message}')

        should_respond = not message.reply_to_message or message.reply_to_message.from_user.id == bot.id

        if should_respond:
            processing_message = await message.reply("Пожалуйста, подождите, я обрабатываю ваш запрос...")
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages[username],
                max_tokens=2500,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                user=username
            )
            chatgpt_response = completion.choices[0]['message']
            messages[username].append({"role": "assistant", "content": chatgpt_response['content']})
            logging.info(f'ChatGPT response: {chatgpt_response["content"]}')
            await message.reply(chatgpt_response['content'])
            await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
    except Exception as e:
        logging.error(f'Error in echo_msg: {e}')


if __name__ == '__main__':
    executor.start_polling(dp)
