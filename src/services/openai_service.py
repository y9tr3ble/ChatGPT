from openai import AsyncOpenAI
from typing import List, Dict, Any
from logging import getLogger

logger = getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("OpenAI API key is required")
        self.client = AsyncOpenAI(api_key=api_key)

    async def generate_chat_response(self, messages: List[Dict[str, str]], user_id: str) -> str:
        try:
            completion = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=2500,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0,
                user=user_id
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error for user {user_id}: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")

    async def generate_image(self, prompt: str) -> str:
        if not prompt:
            raise ValueError("Image prompt cannot be empty")
            
        try:
            response = await self.client.images.generate(
                prompt=prompt,
                n=1,
                size="512x512",
                response_format="url"
            )
            return response.data[0].url
        except Exception as e:
            logger.error(f"Image generation error for prompt '{prompt}': {str(e)}")
            raise Exception(f"Image generation error: {str(e)}") 