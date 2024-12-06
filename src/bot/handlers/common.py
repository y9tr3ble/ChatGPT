from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.services.message_service import MessageService

router = Router(name='common')

__all__ = ['router']

@router.message(Command("start"))
async def start_cmd(message: Message, message_service: MessageService):
    await message_service.send_message(message.from_user.id, "start", message)

@router.message(Command("help"))
async def help_cmd(message: Message, message_service: MessageService):
    await message_service.send_message(message.from_user.id, "help", message)

@router.message(Command("about"))
async def about_cmd(message: Message, message_service: MessageService):
    await message_service.send_message(message.from_user.id, "about", message) 