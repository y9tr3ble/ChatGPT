from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English🇬🇧", callback_data="en"),
            InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"),
            InlineKeyboardButton(text="Український🇺🇦", callback_data="ua")
        ]
    ])
    return keyboard 