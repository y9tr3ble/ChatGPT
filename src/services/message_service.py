from typing import Dict, Optional, List, Union
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from src.bot.message_templates import message_templates
from src.services.storage_service import StorageService
import os
import logging
import asyncio
from collections import deque
import html

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, storage: StorageService, max_messages: int = 20, max_tokens: int = 4000):
        self.message_templates = message_templates
        self.user_languages: Dict[int, str] = {}
        self.messages: Dict[str, List[Dict[str, str]]] = {}
        self.storage = storage
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.message_queue: Dict[int, deque] = {}
        self.MAX_MESSAGE_LENGTH = 4096  # Telegram's max message length
        
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return html.escape(text)
        
    def _format_code_block(self, code: str, language: str = "") -> str:
        """Format code block with proper HTML tags and syntax highlighting hint"""
        escaped_code = self._escape_html(code)
        if language:
            return f'<pre><code class="{language}">{escaped_code}</code></pre>'
        return f'<pre><code>{escaped_code}</code></pre>'
        
    def _format_inline_code(self, code: str) -> str:
        """Format inline code with proper HTML tags"""
        escaped_code = self._escape_html(code)
        return f'<code>{escaped_code}</code>'
        
    def _split_long_message(self, text: str) -> List[str]:
        """Split long messages into chunks respecting code blocks and markdown"""
        if len(text) <= self.MAX_MESSAGE_LENGTH:
            return [text]
            
        chunks = []
        current_chunk = ""
        in_code_block = False
        
        lines = text.split('\n')
        
        for line in lines:
            # Check if this line would exceed the limit
            if len(current_chunk) + len(line) + 1 > self.MAX_MESSAGE_LENGTH:
                if in_code_block:
                    current_chunk += '</code></pre>'
                chunks.append(current_chunk)
                current_chunk = ""
                if in_code_block:
                    current_chunk += '<pre><code>'
                    
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                if in_code_block:
                    current_chunk += '<pre><code>'
                else:
                    current_chunk += '</code></pre>'
            else:
                current_chunk += line + '\n'
                
        if current_chunk:
            if in_code_block:
                current_chunk += '</code></pre>'
            chunks.append(current_chunk)
            
        return chunks
        
    async def _send_message_safe(self, 
        message: types.Message,
        text: str,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]] = None,
        retry_count: int = 3
    ) -> bool:
        """Send message with retries and error handling"""
        for attempt in range(retry_count):
            try:
                await message.answer(
                    text,
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
                return True
            except Exception as e:
                if attempt == retry_count - 1:  # Last attempt
                    logger.error(f"Failed to send message after {retry_count} attempts: {str(e)}")
                    # Try without HTML formatting as last resort
                    try:
                        plain_text = text.replace('<pre><code>', '').replace('</code></pre>', '')
                        plain_text = plain_text.replace('<code>', '').replace('</code>', '')
                        await message.answer(plain_text, reply_markup=reply_markup)
                        return True
                    except Exception as e2:
                        logger.error(f"Failed to send plain text message: {str(e2)}")
                        return False
                await asyncio.sleep(1)  # Wait before retry
        return False

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
            
        # Handle inline code blocks (between single backticks)
        while '`' in text and text.count('`') >= 2:
            start = text.find('`')
            end = text.find('`', start + 1)
            if start != -1 and end != -1:
                code = text[start + 1:end]
                text = text[:start] + self._format_inline_code(code) + text[end + 1:]
            
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
                        if first_line.strip() in ["cpp", "c++", "python", "js", "javascript", "html", "css", "java", "rust", "go"]:
                            code = "\n".join(code_part.split("\n")[1:])
                            lang = first_line.strip()
                        else:
                            code = code_part
                            lang = ""
                    else:
                        code = code_part
                        lang = ""
                    
                    # Format code block
                    formatted_text += "\n" + self._format_code_block(code, lang) + "\n"
                    
                    # Add text between code blocks
                    if i + 1 < len(parts):
                        formatted_text += parts[i + 1]
            
            text = formatted_text
            
        # Split long messages
        message_parts = self._split_long_message(text)
        
        # Send each part
        for part in message_parts:
            success = await self._send_message_safe(message, part, reply_markup if part == message_parts[-1] else None)
            if not success:
                logger.error(f"Failed to send message part to user {user_id}")
                # Send error message to user
                await self._send_message_safe(
                    message,
                    self.get_message("error", self.get_user_language(user_id)),
                    None
                )
                break
            # Small delay between parts to prevent flooding
            if len(message_parts) > 1:
                await asyncio.sleep(0.5)

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