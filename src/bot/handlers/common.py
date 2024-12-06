from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.services.message_service import MessageService
from src.services.user_service import UserService
from src.bot.keyboards import get_main_keyboard, get_model_keyboard

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

@router.message(Command("help"))
@router.message(F.text.contains("❓"))
async def help_cmd(message: Message, message_service: MessageService):
    """Help command handler"""
    await message_service.send_message(
        message.from_user.id,
        "help",
        message
    )

@router.message(Command("about"))
@router.message(F.text.contains("ℹ️"))
async def about_cmd(message: Message, message_service: MessageService):
    """About command handler"""
    await message_service.send_message(
        message.from_user.id,
        "about",
        message
    )

@router.message(Command("stats"))
async def stats_cmd(message: Message, message_service: MessageService, user_service: UserService):
    """Show chat statistics"""
    user_id = str(message.from_user.id)
    stats = message_service.get_message_stats(user_id)
    model = user_service.get_user_model(user_id)
    
    await message_service.send_message(
        message.from_user.id,
        "stats",
        message,
        messages=stats["message_count"],
        tokens=stats["estimated_tokens"],
        max_messages=stats["max_messages"],
        max_tokens=stats["max_tokens"],
        model=model.upper()
    )

@router.message(Command("model"))
@router.message(F.text.contains("🔄"))
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
async def process_model_callback(callback: CallbackQuery, message_service: MessageService, user_service: UserService):
    """Model selection callback handler"""
    user_id = str(callback.from_user.id)
    model = callback.data.replace("model_", "")
    
    # Save user's model choice
    user_service.set_user_model(user_id, model)
    
    # Send confirmation with main keyboard
    lang = message_service.get_user_language(callback.from_user.id)
    keyboard = get_main_keyboard(lang)
    
    # Get message key based on model
    msg_key = f"model_switched_{model}"
    
    await message_service.send_message(
        callback.from_user.id,
        msg_key,
        callback.message,
        reply_markup=keyboard
    )
    
    await callback.answer()

@router.message(Command("newtopic"))
@router.message(F.text.contains("🆕"))
async def new_topic_cmd(message: Message, message_service: MessageService):
    """New topic command handler"""
    user_id = str(message.from_user.id)
    message_service.clear_messages(user_id)
    await message_service.send_message(
        message.from_user.id,
        "new_topic",
        message
    )

@router.message(Command("image"))
@router.message(F.text.contains("🎨"))
async def image_cmd(message: Message, message_service: MessageService):
    """Image generation command handler"""
    await message_service.send_message(
        message.from_user.id,
        "image_prompt",
        message
    ) 