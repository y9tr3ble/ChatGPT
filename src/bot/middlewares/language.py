from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.services.message_service import MessageService

class LanguageMiddleware(BaseMiddleware):
    def __init__(self, message_service: MessageService):
        self.message_service = message_service

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data["message_service"] = self.message_service
        return await handler(event, data) 