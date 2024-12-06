from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.services.message_service import MessageService
from src.services.user_service import UserService
from src.bot.keyboards import get_main_keyboard, get_model_keyboard, get_language_keyboard

router = Router(name='common')

@router.message(Command("start"))
async def start_cmd(message: Message, message_service: MessageService):
    """Start command handler"""
    user_id = str(message.from_user.id)
    message_service.load_user_state(user_id)
    
    lang = message_service.get_user_language(message.from_user.id)
    keyboard = get_main_keyboard(lang)
    
    await message_service.send_message(
        message.from_user.id, 
        "start", 
        message,
        reply_markup=keyboard
    )

@router.message(Command("model"))
@router.message(F.text.contains("Change Model"))
@router.message(F.text.contains("Сменить модель"))
@router.message(F.text.contains("Змінити модель"))
async def model_cmd(message: Message, message_service: MessageService, user_service: UserService):
    """Model selection handler"""
    user_id = str(message.from_user.id)
    current_model = user_service.get_user_model(user_id)
    await message_service.send_message(
        message.from_user.id,
        "current_model",
        message,
        reply_markup=get_model_keyboard(),
        model=current_model.upper()
    )

@router.callback_query(F.data.startswith("model_"))
async def process_model_callback(callback: CallbackQuery, user_service: UserService, message_service: MessageService):
    """Model selection callback handler"""
    user_id = str(callback.from_user.id)
    model = callback.data.replace("model_", "")
    user_service.set_user_model(user_id, model)
    
    msg_key = f"model_switched_{model}"
    await message_service.send_message(callback.from_user.id, msg_key, callback.message)
    await callback.answer()

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

@router.message(Command("help"))
async def help_cmd(message: Message, message_service: MessageService):
    """Show help message"""
    lang = message_service.get_user_language(message.from_user.id)
    keyboard = get_main_keyboard(lang)
    await message_service.send_message(
        message.from_user.id, 
        "help", 
        message,
        reply_markup=keyboard
    )

@router.message(Command("about"))
async def about_cmd(message: Message, message_service: MessageService):
    """About command handler"""
    lang = message_service.get_user_language(message.from_user.id)
    keyboard = get_main_keyboard(lang)
    await message_service.send_message(
        message.from_user.id, 
        "about", 
        message,
        reply_markup=keyboard
    )

@router.message(F.text.startswith('❓'))
async def help_button(message: Message, message_service: MessageService):
    """Help button handler"""
    await help_cmd(message, message_service)

@router.message(F.text.startswith('🌐'))
async def language_button(message: Message, message_service: MessageService):
    """Language button handler"""
    lang = message_service.get_user_language(message.from_user.id)
    keyboard = get_language_keyboard()
    await message_service.send_message(
        message.from_user.id,
        "language_selection",
        message,
        reply_markup=keyboard
    )

@router.message(F.text.startswith('ℹ️'))
async def about_button(message: Message, message_service: MessageService):
    """About button handler"""
    await about_cmd(message, message_service) 