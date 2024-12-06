from aiogram import Router, F
from aiogram.types import Message
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
import logging
from typing import Any

router = Router()

@router.message(F.text)
async def handle_message(
    message: Message,
    message_service: MessageService,
    openai_service: OpenAIService,
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
            # Generate response
            messages = message_service.get_messages(user_id)
            response = await openai_service.generate_chat_response(messages, user_id)
            
            # Add response to history
            message_service.add_message(user_id, "assistant", response)
            
            # Send response
            await message.answer(response)
            
        except Exception as e:
            logging.error(f"OpenAI error: {str(e)}")
            await message.answer(
                message_service.get_message("error", message_service.get_user_language(message.from_user.id))
            )
        finally:
            # Always try to delete processing message
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