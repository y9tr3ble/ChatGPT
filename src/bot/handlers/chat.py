from aiogram import Router, F
from aiogram.types import Message
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
from src.services.gemini_service import GeminiService
from src.services.gpt4o_service import GPT4OService
from src.services.user_service import UserService
from src.bot.keyboards import get_main_keyboard
import logging
from typing import Any

router = Router()

@router.message(F.text)
async def handle_message(
    message: Message,
    message_service: MessageService,
    openai_service: OpenAIService,
    gemini_service: GeminiService,
    gpt4o_service: GPT4OService,
    user_service: UserService,
    **data: Any
) -> None:
    try:
        user_id = str(message.from_user.id)
        
        # Load user state from storage
        message_service.load_user_state(user_id)
        
        # Игнорируем команды кнопок
        if message.text.startswith(('❓', '🔄', '🌐', 'ℹ️')):
            return
        
        # Add message to history
        message_service.add_message(user_id, "user", message.text)
        
        # Get processing message
        processing_msg = await message.answer(
            message_service.get_message("processing", message_service.get_user_language(message.from_user.id))
        )
        
        try:
            # Get messages history
            messages = message_service.get_messages(user_id)
            
            # Choose service based on user preference
            current_model = user_service.get_user_model(user_id)
            if current_model == "gemini":
                response = await gemini_service.generate_chat_response(messages, user_id)
            elif current_model == "gpt4":
                response = await openai_service.generate_chat_response(messages, user_id)
            elif current_model == "gpt4o":
                response = await gpt4o_service.generate_chat_response(messages, user_id, is_mini=False)
            else:  # gpt4o_mini
                response = await gpt4o_service.generate_chat_response(messages, user_id, is_mini=True)
            
            # Add response to history
            message_service.add_message(user_id, "assistant", response)
            
            # Send response with keyboard
            lang = message_service.get_user_language(message.from_user.id)
            keyboard = get_main_keyboard(lang)
            await message.answer(response, reply_markup=keyboard)
            
        except ValueError as ve:
            if str(ve) == "safety_error":
                # Отправляем сообщение о нарушении правил безопасности
                await message_service.send_message(
                    message.from_user.id,
                    "safety_error",
                    message,
                    reply_markup=get_main_keyboard(message_service.get_user_language(message.from_user.id))
                )
            else:
                raise
            
        except Exception as e:
            if not isinstance(e, ValueError) or str(e) != "safety_error":
                logging.error(f"{current_model.upper()} API error: {str(e)}")
                await message.answer(
                    message_service.get_message("error", message_service.get_user_language(message.from_user.id))
                )
        finally:
            try:
                await processing_msg.delete()
            except Exception as e:
                logging.error(f"Error deleting processing message: {str(e)}")
        
    except Exception as e:
        logging.error(f"Error in handle_message: {str(e)}")
        try:
            await message.answer(
                message_service.get_message("error", message_service.get_user_language(message.from_user.id))
            )
        except Exception as send_error:
            logging.error(f"Error sending error message: {str(send_error)}") 