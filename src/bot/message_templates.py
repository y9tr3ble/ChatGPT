from typing import Dict, Any

message_templates: Dict[str, Dict[str, str]] = {
    'en': {
        'start': """ Hello! I'm a smart assistant powered by AI.

I can help you with various tasks using two powerful AI models:
• OpenAI GPT-4 🤖
• Google Gemini ✨

Use the buttons below to interact with me!""",
        'help': """🔍 <b>Available Commands:</b>

/start - Start bot
/help - Show this help
/about - About bot
/language - Change language
/model - Show current AI model

You can also use the buttons below for quick access to commands.""",
        'about': """🤖 <b>AI Assistant Bot</b>

This bot combines the power of two leading AI models:
• OpenAI GPT-4
• Google Gemini

Version: 1.0
Developer: @your_username""",
        'new_topic': 'Starting a new topic!',
        'image_prompt': 'Please add a description of the image after the /image command.',
        'image_error': 'An error occurred during image generation:',
        'language_confirmation': "Language has been set to English.",
        'language_selection': "Choose your language:",
        'processing': "Processing your request...",
        'error': "An error occurred. Please try again later.",
        'model_switched_gemini': "Switched to Gemini model ✨",
        'model_switched_openai': "Switched to OpenAI model 🤖",
        'current_model': "Current model: {model}",
        'safety_error': """⚠️ I cannot process this request due to content safety guidelines.
Please rephrase your message to be more appropriate and try again.

Guidelines:
• Avoid sensitive topics
• Keep the conversation respectful
• No explicit content""",
    },
    'ru': {
        'start': "Привет, я бот на основе API GPT-4(ChatGPT). Введите /help",
        'new_topic': 'Начинаем новую тему!',
        'image_prompt': 'Пожалуйста, добавьте описание изображения после команды /image.',
        'image_error': 'Произошла ошибка при генерации изображения:',
        'about': 'Этот бот работает на основе OpenAI GPT-4.',
        'help': '''Доступные команды:
/start - Запустить бота
/help - Показать справку
/about - О боте
/language - Изменить язык
/model - Показать текущую модель
/use_openai - Переключиться на OpenAI
/use_gemini - Переключиться на Gemini
''',
        'language_confirmation': "Язык установлен на русский.",
        'language_selection': "Выберите язык:",
        'processing': "Обрабатываю ваш запрос...",
        'error': "Произошла ошибка. Пожалуйста, попробуйте позже.",
        'model_switched_gemini': "Переключено на модель Gemini ✨",
        'model_switched_openai': "Переключено на модель OpenAI 🤖",
        'current_model': "Текущая модель: {model}",
        'safety_error': """⚠️ Я не могу обработать этот запрос из-за правил безопасности контента.
Пожалуйста, перефразируйте сообщение более корректно и попробуйте снова.

Рекомендации:
• Избегайте чувствительных тем
• Соблюдайте уважительный тон
• Без неприемлемого контента""",
    },
    'ua': {
        'start': "Привіт, я бот на основі API GPT-4(ChatGPT). Введіть /help",
        'new_topic': 'Починаємо нову тему!',
        'image_prompt': 'Будь ласка, додайте опис зображення після команди /image.',
        'image_error': 'Виникла помилка під час генерації зображення:',
        'about': 'Цей бот працює на основі OpenAI GPT-4.',
        'help': '''Доступні команди:
/start - Запустити бота
/help - Показати довідку
/about - Про бота
/language - Змінити мову
/model - Показати поточну модель
/use_openai - Перемкнутися на OpenAI
/use_gemini - Перемкнутися на Gemini
''',
        'language_confirmation': "Мову встановлено на українську.",
        'language_selection': "Оберіть мову:",
        'processing': "Обробляю ваш запит...",
        'error': "Сталася помилка. Будь ласка, спробуйте пізніше.",
        'model_switched_gemini': "Переключено на модель Gemini ✨",
        'model_switched_openai': "Переключено на модель OpenAI 🤖",
        'current_model': "Поточна модель: {model}",
        'safety_error': """⚠️ Я не можу обробити цей запит через правила безпеки контенту.
Будь ласка, перефразуйте повідомлення більш коректно та спробуйте знову.

Рекомендації:
• Уникайте чутливих тем
• Дотримуйтесь шанобливого тону
• Без неприйнятного контенту""",
    }
}

__all__ = ['message_templates'] 