from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from src.services.message_service import MessageService
from src.services.user_service import UserService

router = Router(name='common')

@router.message(Command("model"))
async def show_model(message: Message, message_service: MessageService, user_service: UserService):
    """Show current model"""
    user_id = str(message.from_user.id)
    current_model = user_service.get_user_model(user_id)
    await message_service.send_message(
        message.from_user.id, 
        "current_model", 
        message, 
        model=current_model.upper()
    )

@router.message(Command("use_gemini"))
async def use_gemini(message: Message, message_service: MessageService, user_service: UserService):
    """Switch to Gemini model"""
    user_id = str(message.from_user.id)
    user_service.set_user_model(user_id, "gemini")
    await message_service.send_message(message.from_user.id, "model_switched_gemini", message)

@router.message(Command("use_openai"))
async def use_openai(message: Message, message_service: MessageService, user_service: UserService):
    """Switch to OpenAI model"""
    user_id = str(message.from_user.id)
    user_service.set_user_model(user_id, "openai")
    await message_service.send_message(message.from_user.id, "model_switched_openai", message)

@router.message(Command("start"))
async def start_cmd(message: Message, message_service: MessageService):
    await message_service.send_message(message.from_user.id, "start", message)

@router.message(Command("help"))
async def help_cmd(message: Message, message_service: MessageService):
    """Show help message"""
    await message_service.send_message(message.from_user.id, "help", message)

@router.message(Command("about"))
async def about_cmd(message: Message, message_service: MessageService):
    await message_service.send_message(message.from_user.id, "about", message) 