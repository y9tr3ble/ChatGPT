import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
from config import bot_token, api_key
from message_templates import message_templates

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

openai.api_key = api_key

messages = {}
user_languages = {}  # Keep track of user's current language


@dp.callback_query_handler(lambda c: c.data in ['en', 'ru', 'ua'])
async def process_callback(callback_query: types.CallbackQuery):
    user_languages[callback_query.from_user.id] = callback_query.data
    await send_message(callback_query.from_user.id, 'language_confirmation')
    await bot.answer_callback_query(callback_query.id)


# Create language selection keyboard
language_keyboard = InlineKeyboardMarkup(row_width=2)
language_keyboard.add(InlineKeyboardButton("English🇬🇧", callback_data='en'),
                      InlineKeyboardButton("Русский🇷🇺", callback_data='ru'),
                      InlineKeyboardButton("Український🇺🇦", callback_data='ua'))


async def send_message(user_id, message_key):
    language = user_languages.get(user_id, 'en')  # Default to English
    message_template = message_templates[language][message_key]
    await bot.send_message(user_id, message_template)


@dp.message_handler(commands=['language'])
async def language_cmd(message: types.Message):
    await bot.send_message(message.chat.id, message_templates['en']['language_selection'],
                           reply_markup=language_keyboard)


@dp.callback_query_handler(lambda c: c.data in ['en', 'ru'])
async def process_callback(callback_query: types.CallbackQuery):
    user_languages[callback_query.from_user.id] = callback_query.data
    await bot.answer_callback_query(callback_query.id)


async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )

    return response['data'][0]['url']


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    try:
        username = message.from_user.username
        messages[username] = []
        language = user_languages.get(message.from_user.id, 'en')  # Get the selected language
        await message.reply(message_templates[language]['start'])  # Retrieve the correct message based on the language
    except Exception as e:
        logging.error(f'Error in start_cmd: {e}')


@dp.message_handler(commands=['newtopic'])
async def new_topic_cmd(message: types.Message):
    try:
        userid = message.from_user.id
        messages[str(userid)] = []
        language = user_languages.get(message.from_user.id, 'en')
        await message.reply(message_templates[language]['newtopic'])
    except Exception as e:
        logging.error(f'Error in new_topic_cmd: {e}')


@dp.message_handler(commands=['image'])
async def send_image(message: types.Message):
    try:
        description = message.text.replace('/image', '').strip()
        language = user_languages.get(message.from_user.id, 'en')
        if not description:
            await message.reply(message_templates[language]['image_prompt'])
            return
    except Exception as e:
        logging.error(f'Error in send_image: {e}')
    try:
        image_url = await generate_image(description)
        await bot.send_photo(chat_id=message.chat.id, photo=image_url)
    except Exception as e:
        await message.reply(message_templates[language]['image_error'] + str(e))


@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply(message_templates[language]['help'])


@dp.message_handler(commands=['about'])
async def about_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply(message_templates[language]['about'])


@dp.message_handler()
async def echo_msg(message: types.Message):
    try:
        user_message = message.text
        userid = message.from_user.username

        if userid not in messages:
            messages[userid] = []
        messages[userid].append({"role": "user", "content": user_message})
        messages[userid].append({"role": "user",
                                 "content": f"chat: {message.chat} Now {time.strftime('%d/%m/%Y %H:%M:%S')} user: {message.from_user.first_name} message: {message.text}"})
        logging.info(f'{userid}: {user_message}')

        should_respond = not message.reply_to_message or message.reply_to_message.from_user.id == bot.id

        if should_respond:
            language = user_languages.get(message.from_user.id, 'en')
            processing_message = await message.reply(message_templates[language]['processing'])

            await bot.send_chat_action(chat_id=message.chat.id, action="typing")

            completion = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=messages[userid],
                max_tokens=2500,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                user=userid
            )
            chatgpt_response = completion.choices[0]['message']

            messages[userid].append({"role": "assistant", "content": chatgpt_response['content']})
            logging.info(f'ChatGPT response: {chatgpt_response["content"]}')

            await message.reply(chatgpt_response['content'])

            await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)

    except Exception as ex:
        if ex == "context_length_exceeded":
            language = user_languages.get(message.from_user.id, 'en')
            await message.reply(message_templates[language]['error'])
            await new_topic_cmd(message)
            await echo_msg(message)


if __name__ == '__main__':
    executor.start_polling(dp)
