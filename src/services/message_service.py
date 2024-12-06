from typing import Dict, Optional, List, Union
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from src.bot.message_templates import message_templates
from src.services.storage_service import StorageService
import os
import logging

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, storage: StorageService, max_messages: int = 20, max_tokens: int = 4000):
        self.message_templates = message_templates
        self.user_languages: Dict[int, str] = {}
        self.messages: Dict[str, List[Dict[str, str]]] = {}
        self.storage = storage
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        
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
            
        # Add new message
        message = {"role": role, "content": content}
        self.messages[user_id].append(message)
        
        # Check message count limit
        if len(self.messages[user_id]) > self.max_messages:
            # Remove oldest messages but keep the system message if it exists
            if self.messages[user_id][0]["role"] == "system":
                self.messages[user_id] = [self.messages[user_id][0]] + self.messages[user_id][-self.max_messages+1:]
            else:
                self.messages[user_id] = self.messages[user_id][-self.max_messages:]
        
        # Estimate token count (rough estimation)
        total_tokens = sum(len(msg["content"].split()) * 1.3 for msg in self.messages[user_id])
        
        # If exceeding token limit, remove oldest messages
        while total_tokens > self.max_tokens and len(self.messages[user_id]) > 1:
            # Keep system message if it exists
            if self.messages[user_id][0]["role"] == "system" and len(self.messages[user_id]) > 2:
                removed_msg = self.messages[user_id][1]
                self.messages[user_id].pop(1)
            else:
                removed_msg = self.messages[user_id][0]
                self.messages[user_id].pop(0)
            total_tokens -= len(removed_msg["content"].split()) * 1.3
            
        self.save_user_state(user_id)
        
        # Log message stats
        logger.info(f"User {user_id} messages: {len(self.messages[user_id])}, estimated tokens: {int(total_tokens)}")

    def get_messages(self, user_id: str) -> List[Dict[str, str]]:
        """Get all messages for user"""
        return self.messages.get(user_id, [])
        
    def get_message_stats(self, user_id: str) -> Dict[str, int]:
        """Get message statistics for user"""
        messages = self.messages.get(user_id, [])
        total_tokens = sum(len(msg["content"].split()) * 1.3 for msg in messages)
        return {
            "message_count": len(messages),
            "estimated_tokens": int(total_tokens),
            "max_messages": self.max_messages,
            "max_tokens": self.max_tokens
        }

    async def send_message(
        self, 
        user_id: int, 
        message_key_or_text: str, 
        message: types.Message, 
        reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None] = None,
        is_response: bool = False,
        **kwargs
    ) -> None:
        """Send message to user using template with optional formatting and keyboard"""
        # If it's a template key, get the template
        if not is_response:
            language = self.get_user_language(user_id)
            text = self.get_message(message_key_or_text, language)
            
            # Format message if kwargs provided
            if kwargs:
                text = text.format(**kwargs)
        else:
            # If it's a direct response, use the text as is
            text = message_key_or_text
            
        # Handle code blocks for Telegram formatting
        if "```" in text:
            # Split text by code blocks
            parts = text.split("```")
            formatted_text = parts[0]  # First part (before any code block)
            
            for i in range(1, len(parts), 2):
                if i < len(parts):
                    # Extract code and language (if specified)
                    code_part = parts[i].strip()
                    if code_part and "\n" in code_part:
                        first_line = code_part.split("\n")[0]
                        if first_line.strip() in ["cpp", "c++", "python", "js", "javascript"]:
                            code = "\n".join(code_part.split("\n")[1:])
                            lang = first_line.strip()
                        else:
                            code = code_part
                            lang = ""
                    else:
                        code = code_part
                        lang = ""
                    
                    # Escape HTML special characters in code
                    code = code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    
                    # Format code block with HTML and proper spacing
                    formatted_text += f"\n<pre><code>{code}</code></pre>\n"
                    
                    # Add text between code blocks
                    if i + 1 < len(parts):
                        formatted_text += parts[i + 1]
            
            text = formatted_text
        
        # Send message
        try:
            await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        except Exception as e:
            # If HTML parsing fails, try sending without code formatting
            logging.error(f"Error sending formatted message: {str(e)}")
            text = text.replace("<pre><code>", "").replace("</code></pre>", "")
            await message.answer(text, reply_markup=reply_markup)

    def clear_all_messages(self) -> None:
        """Clear all messages for all users"""
        self.messages = {}
        # Clear messages in storage for all users
        storage_dir = self.storage.storage_dir
        if os.path.exists(storage_dir):
            for filename in os.listdir(storage_dir):
                if filename.startswith("user_") and filename.endswith(".json"):
                    user_id = filename[5:-5]  # Extract user ID from filename
                    data = self.storage.load_user_data(user_id)
                    if data:
                        data['messages'] = []
                        self.storage.save_user_data(user_id, data) 