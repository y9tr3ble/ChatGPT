from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.bot.keyboards import get_language_keyboard
from src.services.message_service import MessageService

router = Router(name='language')

__all__ = ['router']

@router.message(Command("language"))
async def language_cmd(message: Message, message_service: MessageService):
    await message.answer(
        message_service.get_message("language_selection", message_service.get_user_language(message.from_user.id)),
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.in_({"en", "ru", "ua"}))
async def process_language_callback(callback: CallbackQuery, message_service: MessageService):
    await message_service.set_user_language(callback.from_user.id, callback.data)
    await callback.message.answer(
        message_service.get_message("language_confirmation", callback.data)
    )
    await callback.answer() 