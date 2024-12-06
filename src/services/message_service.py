from typing import Dict, Optional, List, Union
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from src.bot.message_templates import message_templates
from src.services.storage_service import StorageService
import os

class MessageService:
    def __init__(self, storage: StorageService):
        self.message_templates = message_templates
        self.user_languages: Dict[int, str] = {}
        self.messages: Dict[str, List[Dict[str, str]]] = {}
        self.storage = storage
        
    def load_user_state(self, user_id: str) -> None:
        """Load user state from storage"""
        data = self.storage.load_user_data(user_id)
        if data:
            if 'language' in data:
                self.user_languages[int(user_id)] = data['language']
            if 'messages' in data:
                self.messages[user_id] = data['messages']
        
    def save_user_state(self, user_id: str) -> None:
        """Save user state to storage"""
        data = {
            'language': self.user_languages.get(int(user_id), 'en'),
            'messages': self.messages.get(user_id, [])
        }
        self.storage.save_user_data(user_id, data)

    def get_user_language(self, user_id: int) -> str:
        """Get user's language or return default language (en)"""
        return self.user_languages.get(user_id, 'en')

    async def set_user_language(self, user_id: int, language: str) -> None:
        """Set user's preferred language and save state"""
        if language not in self.message_templates:
            raise ValueError(f"Unsupported language: {language}")
        self.user_languages[user_id] = language
        self.save_user_state(str(user_id))

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
        self.save_user_state(user_id)

    def add_message(self, user_id: str, role: str, content: str) -> None:
        """Add message to user's history and save state"""
        if user_id not in self.messages:
            self.messages[user_id] = []
        self.messages[user_id].append({"role": role, "content": content})
        self.save_user_state(user_id)

    def get_messages(self, user_id: str) -> List[Dict[str, str]]:
        """Get all messages for user"""
        return self.messages.get(user_id, [])

    async def send_message(
        self, 
        user_id: int, 
        message_key: str, 
        message: types.Message, 
        reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None] = None,
        **kwargs
    ) -> None:
        """Send message to user using template with optional formatting and keyboard"""
        language = self.get_user_language(user_id)
        text = self.get_message(message_key, language)
        
        # Format message if kwargs provided
        if kwargs:
            text = text.format(**kwargs)
        
        await message.reply(text, reply_markup=reply_markup) 

    def clear_all_messages(self) -> None:
        """Clear all messages for all users"""
        self.messages = {}
        # Очищаем сообщения в хранилище для всех пользователей
        storage_dir = self.storage.storage_dir
        if os.path.exists(storage_dir):
            for filename in os.listdir(storage_dir):
                if filename.startswith("user_") and filename.endswith(".json"):
                    user_id = filename[5:-5]  # Извлекаем ID пользователя из имени файла
                    data = self.storage.load_user_data(user_id)
                    if data:
                        data['messages'] = []
                        self.storage.save_user_data(user_id, data) 