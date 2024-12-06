from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.services.message_service import MessageService
from src.bot.keyboards import get_language_keyboard, get_main_keyboard

router = Router(name='language')

__all__ = ['router']

@router.message(Command("language"))
@router.message(F.text.contains("Language"))
@router.message(F.text.contains("Язык"))
@router.message(F.text.contains("Мова"))
async def language_cmd(message: Message, message_service: MessageService):
    """Language selection handler"""
    await message_service.send_message(
        message.from_user.id,
        "language_selection",
        message,
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.in_({"en", "ru", "ua"}))
async def process_language_callback(callback: CallbackQuery, message_service: MessageService):
    """Language selection callback handler"""
    user_id = str(callback.from_user.id)
    message_service.load_user_state(user_id)
    
    # Устанавливаем новый язык
    await message_service.set_user_language(callback.from_user.id, callback.data)
    
    # Отправляем подтверждение с новой клавиатурой
    keyboard = get_main_keyboard(callback.data)
    await message_service.send_message(
        callback.from_user.id,
        "language_confirmation",
        callback.message,
        reply_markup=keyboard
    )
    
    # Закрываем меню выбора языка
    await callback.answer() 