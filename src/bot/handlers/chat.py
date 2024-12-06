from aiogram import Router, F
from aiogram.types import Message
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
from src.services.gemini_service import GeminiService
from src.services.user_service import UserService
import logging
from typing import Any

router = Router()

@router.message(F.text)
async def handle_message(
    message: Message,
    message_service: MessageService,
    openai_service: OpenAIService,
    gemini_service: GeminiService,
    user_service: UserService,
    **data: Any
) -> None:
    try:
        user_id = str(message.from_user.id)
        
        # Skip if message is empty
        if not message.text:
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
            service = gemini_service if current_model == "gemini" else openai_service
            
            # Generate response
            response = await service.generate_chat_response(messages, user_id)
            
            # Add response to history
            message_service.add_message(user_id, "assistant", response)
            
            # Send response
            await message.answer(response)
            
        except Exception as e:
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