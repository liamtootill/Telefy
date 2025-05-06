import httpx
import os
import logging
from typing import Optional

# Import settings
from .config import settings

logger = logging.getLogger(__name__)

# BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # Replaced by settings
if not settings or not settings.TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not found in settings. Cannot send messages or fetch bot info.")
    # Allow running, but functions will fail

BOT_USERNAME: Optional[str] = None # To store the bot's username
BOT_USER_ID: Optional[int] = None  # To store the bot's user ID

async def fetch_bot_info():
    """Gets the bot's username and ID using the getMe method and stores them globally."""
    global BOT_USERNAME, BOT_USER_ID # Allow modification of global variables
    if BOT_USERNAME and BOT_USER_ID: # Return if cached already
        logger.debug("Bot info already cached.")
        return
        
    if not settings or not settings.TELEGRAM_BOT_TOKEN:
        logger.error("Cannot get bot info: TELEGRAM_BOT_TOKEN not configured.")
        return

    api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getMe"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, timeout=10.0)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("ok"):
                bot_info = response_data.get("result", {})
                username = bot_info.get("username")
                user_id = bot_info.get("id")
                
                if username and user_id:
                    full_username = f"@{username}"
                    logger.info(f"Successfully retrieved bot info: Username={full_username}, ID={user_id}")
                    BOT_USERNAME = full_username # Cache the username with @
                    BOT_USER_ID = user_id        # Cache the user ID
                else:
                    logger.error(f"Failed to extract username or ID from getMe response: {bot_info}")
            else:
                error_description = response_data.get('description', 'Unknown error')
                status_code = response.status_code
                logger.error(f"Failed to call getMe. Status: {status_code}, Error: {error_description}")
                
    except httpx.RequestError as e:
        logger.error(f"HTTP request failed during getMe call: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during getMe call: {e}")

async def send_telegram_message(chat_id: int, text: str) -> dict:
    """
    Sends a text message to a specific Telegram chat using the Bot API.

    Args:
        chat_id: The target chat ID.
        text: The message text to send.

    Returns:
        A dictionary: {"success": True, "message_id": int} on success,
        or {"success": False} on failure.
    """
    if not settings or not settings.TELEGRAM_BOT_TOKEN:
        logger.error("Cannot send message: TELEGRAM_BOT_TOKEN not configured.")
        return {"success": False}

    api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        # Optional: Add parse_mode="MarkdownV2" or "HTML" if needed
        # "parse_mode": "MarkdownV2" 
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, timeout=10.0)
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get("ok"):
                logger.info(f"Successfully sent message to chat {chat_id}")
                # Extract the message_id of the sent message
                sent_message_id = response_data.get("result", {}).get("message_id")
                if sent_message_id:
                    return {"success": True, "message_id": sent_message_id}
                else:
                    logger.error(f"Sent message OK, but could not extract message_id from response: {response_data}")
                    return {"success": False} # Treat as failure if ID is missing
            else:
                # Log the error description provided by Telegram API
                error_description = response_data.get('description', 'Unknown error')
                status_code = response.status_code
                logger.error(f"Failed to send message to chat {chat_id}. Status: {status_code}, Error: {error_description}")
                logger.debug(f"Telegram API raw error response: {response_data}")
                return {"success": False}
                
    except httpx.RequestError as e:
        logger.error(f"HTTP request failed when sending message to chat {chat_id}: {e}")
        return {"success": False}
    except Exception as e:
        logger.error(f"Unexpected error sending message to chat {chat_id}: {e}")
        return {"success": False} 