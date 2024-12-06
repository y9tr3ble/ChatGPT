import google.generativeai as genai
from typing import List, Dict
import logging

class GeminiService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key is required")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def generate_chat_response(self, messages: List[Dict[str, str]], user_id: str) -> str:
        try:
            # Конвертируем формат сообщений из OpenAI в формат Gemini
            chat = self.model.start_chat(history=[])
            
            for message in messages:
                if message["role"] == "user":
                    response = chat.send_message(message["content"])
                
            return response.text
            
        except Exception as e:
            logging.error(f"Gemini API error for user {user_id}: {str(e)}")
            raise Exception(f"Gemini API error: {str(e)}") 