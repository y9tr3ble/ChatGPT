from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора языка"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="English🇬🇧", callback_data="en"),
            InlineKeyboardButton(text="Русский🇷🇺", callback_data="ru"),
            InlineKeyboardButton(text="Український🇺🇦", callback_data="ua")
        ]
    ])
    return keyboard

def get_model_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора модели"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="GPT-4 🤖", callback_data="model_gpt4"),
            InlineKeyboardButton(text="Google Gemini ✨", callback_data="model_gemini")
        ],
        [
            InlineKeyboardButton(text="GPT-4O 🔮", callback_data="model_gpt4o"),
            InlineKeyboardButton(text="GPT-4O-mini 🎯", callback_data="model_gpt4o_mini")
        ]
    ])
    return keyboard

def get_main_keyboard(lang: str = 'en') -> ReplyKeyboardMarkup:
    """Основная клавиатура с командами"""
    commands = {
        'en': {
            'help': '❓ Help',
            'model': '🔄 Change Model',
            'language': '🌐 Language',
            'about': 'ℹ️ About'
        },
        'ru': {
            'help': '❓ Помощь',
            'model': '🔄 Сменить модель',
            'language': '🌐 Язык',
            'about': 'ℹ️ О боте'
        },
        'ua': {
            'help': '❓ Довідка',
            'model': '🔄 Змінити модель',
            'language': '🌐 Мова',
            'about': 'ℹ️ Про бота'
        }
    }
    
    cmd = commands.get(lang, commands['en'])
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=cmd['help']), KeyboardButton(text=cmd['model'])],
            [KeyboardButton(text=cmd['language']), KeyboardButton(text=cmd['about'])]
        ],
        resize_keyboard=True
    )
    return keyboard 