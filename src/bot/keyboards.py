from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English 🇬🇧", callback_data="en"),
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru"),
            InlineKeyboardButton(text="Українська 🇺🇦", callback_data="ua")
        ]
    ])
    return keyboard

def get_model_keyboard() -> InlineKeyboardMarkup:
    """Model selection keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="GPT-4 🤖", callback_data="model_gpt4"),
            InlineKeyboardButton(text="Gemini ✨", callback_data="model_gemini")
        ],
        [
            InlineKeyboardButton(text="GPT-4O 🔮", callback_data="model_gpt4o"),
            InlineKeyboardButton(text="GPT-4O-mini 🎯", callback_data="model_gpt4o_mini")
        ]
    ])
    return keyboard

def get_main_keyboard(lang: str = 'en') -> ReplyKeyboardMarkup:
    """Main command keyboard with localization"""
    commands = {
        'en': {
            'help': '❓ Help',
            'model': '🔄 Change Model',
            'language': '🌐 Language',
            'about': 'ℹ️ About',
            'new_topic': '🆕 New Topic',
            'image': '🎨 Generate Image'
        },
        'ru': {
            'help': '❓ Помощь',
            'model': '🔄 Сменить модель',
            'language': '🌐 Язык',
            'about': 'ℹ️ О боте',
            'new_topic': '🆕 Новая тема',
            'image': '🎨 Создать изображение'
        },
        'ua': {
            'help': '❓ Довідка',
            'model': '🔄 Змінити модель',
            'language': '🌐 Мова',
            'about': 'ℹ️ Про бота',
            'new_topic': '🆕 Нова тема',
            'image': '🎨 Створити зображення'
        }
    }
    
    cmd = commands.get(lang, commands['en'])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=cmd['help']), 
                KeyboardButton(text=cmd['model'])
            ],
            [
                KeyboardButton(text=cmd['language']), 
                KeyboardButton(text=cmd['about'])
            ],
            [
                KeyboardButton(text=cmd['new_topic']), 
                KeyboardButton(text=cmd['image'])
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Send a message or use buttons below"
    )
    return keyboard 