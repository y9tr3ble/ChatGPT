from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction
from src.services.message_service import MessageService
from src.services.openai_service import OpenAIService
from src.services.gemini_service import GeminiService
from src.services.gpt4o_service import GPT4OService
from src.services.user_service import UserService
import logging

router = Router(name='chat')

@router.message(F.text)
async def handle_message(
    message: Message,
    message_service: MessageService,
    openai_service: OpenAIService,
    gemini_service: GeminiService,
    gpt4o_service: GPT4OService,
    user_service: UserService
):
    """Handle user messages"""
    try:
        user_id = str(message.from_user.id)
        
        # Skip processing commands
        if message.text.startswith('/'):
            return
            
        # Load user state
        message_service.load_user_state(user_id)
        
        # Add user message to history
        message_service.add_message(user_id, "user", message.text)
        
        # Show typing status
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING
        )
        
        # Get current model and generate response
        model = user_service.get_user_model(user_id)
        response = ""
        
        if model == "gpt4":
            response = await openai_service.generate_chat_response(
                message_service.get_messages(user_id),
                user_id
            )
        elif model == "gemini":
            response = await gemini_service.generate_chat_response(
                message_service.get_messages(user_id),
                user_id
            )
        elif model == "gpt4o":
            response = await gpt4o_service.generate_chat_response(
                message_service.get_messages(user_id),
                user_id
            )
        elif model == "gpt4o_mini":
            response = await gpt4o_service.generate_chat_response(
                message_service.get_messages(user_id),
                user_id,
                is_mini=True
            )
            
        # Add response to history
        message_service.add_message(user_id, "assistant", response)
        
        # Send response
        await message_service.send_message(
            message.from_user.id,
            response,
            message,
            is_response=True
        )
        
    except ValueError as e:
        if "safety_error" in str(e):
            await message_service.send_message(
                message.from_user.id,
                "safety_error",
                message
            )
        else:
            logging.error(f"Error processing message: {str(e)}")
            await message_service.send_message(
                message.from_user.id,
                "error",
                message
            )
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        await message_service.send_message(
            message.from_user.id,
            "error",
            message
        ) 