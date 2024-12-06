from typing import Dict, Optional, List
from aiogram import types
from src.bot.message_templates import message_templates

class MessageService:
    def __init__(self):
        self.message_templates = message_templates
        self.user_languages: Dict[int, str] = {}
        self.messages: Dict[str, List[Dict[str, str]]] = {}

    def get_user_language(self, user_id: int) -> str:
        """Get user's language or return default language (en)"""
        return self.user_languages.get(user_id, 'en')

    async def set_user_language(self, user_id: int, language: str) -> None:
        """Set user's preferred language"""
        if language not in self.message_templates:
            raise ValueError(f"Unsupported language: {language}")
        self.user_languages[user_id] = language

    def get_message(self, key: str, language: str) -> str:
        """Get message template by key and language"""
        try:
            return self.message_templates[language][key]
        except KeyError:
            # Fallback to English if translation is missing
            return self.message_templates['en'][key]

    def clear_messages(self, user_id: str) -> None:
        """Clear message history for user"""
        self.messages[user_id] = []

    def add_message(self, user_id: str, role: str, content: str) -> None:
        """Add message to user's history"""
        if user_id not in self.messages:
            self.messages[user_id] = []
        self.messages[user_id].append({"role": role, "content": content})

    def get_messages(self, user_id: str) -> List[Dict[str, str]]:
        """Get all messages for user"""
        return self.messages.get(user_id, [])

    async def send_message(self, user_id: int, message_key: str, message: types.Message, **kwargs) -> None:
        """Send message to user using template with optional formatting"""
        language = self.get_user_language(user_id)
        text = self.get_message(message_key, language)
        
        # Format message if kwargs provided
        if kwargs:
            text = text.format(**kwargs)
        
        await message.reply(text) 