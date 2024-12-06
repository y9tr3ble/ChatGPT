from openai import AsyncOpenAI
from typing import List, Dict, Any
from logging import getLogger

logger = getLogger(__name__)

class GPT4OService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.client = AsyncOpenAI(api_key=api_key)
        
    async def generate_chat_response(self, messages: List[Dict[str, str]], user_id: str, is_mini: bool = False) -> str:
        try:
            model = "gpt-4o-mini" if is_mini else "gpt-4o"
            completion = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=2500,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                user=user_id
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"GPT-4O API error for user {user_id}: {str(e)}")
            raise Exception(f"GPT-4O API error: {str(e)}") 