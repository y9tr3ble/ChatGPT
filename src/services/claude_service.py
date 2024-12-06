from anthropic import Anthropic
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ClaudeService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Anthropic API key is required")
        self.client = Anthropic(api_key=api_key)
        
    async def generate_chat_response(self, messages: List[Dict[str, str]], user_id: str, is_haiku: bool = False) -> str:
        try:
            # Convert message history to Claude format
            formatted_messages = []
            for msg in messages:
                role = "assistant" if msg["role"] == "assistant" else "user"
                formatted_messages.append({"role": role, "content": msg["content"]})
            
            # Choose model based on type
            model = "claude-3-5-haiku-latest" if is_haiku else "claude-3-5-sonnet-latest"
            
            # Create message
            message = await self.client.messages.create(
                model=model,
                max_tokens=2048,
                messages=formatted_messages,
                temperature=0.7
            )
            
            return message.content[0].text
            
        except Exception as e:
            logger.error(f"Claude API error for user {user_id}: {str(e)}")
            raise Exception(f"Claude API error: {str(e)}")
            
    async def generate_haiku_response(self, messages: List[Dict[str, str]], user_id: str) -> str:
        """Generate response using Claude Haiku model"""
        return await self.generate_chat_response(messages, user_id, is_haiku=True) 