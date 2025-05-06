# Placeholder for Telegram bot listener logic using aiogram
# This might run as a separate persistent process

import asyncio
import logging
import os
import httpx

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Update

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get bot token and API base URL from environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000") # Default for local dev

if not BOT_TOKEN:
    logging.error("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
    exit()

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def forward_to_api(update: Update):
    """Forwards the relevant update data to the FastAPI backend."""
    api_endpoint = f"{API_BASE_URL}/api/webhook"
    try:
        async with httpx.AsyncClient() as client:
            # Convert the Update object to a dictionary for JSON serialization
            update_data = update.model_dump(mode='json') # Use model_dump for pydantic v2
            response = await client.post(api_endpoint, json=update_data, timeout=10.0)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            logging.info(f"Successfully forwarded update to API. Status: {response.status_code}")
    except httpx.RequestError as e:
        logging.error(f"Could not forward update to API: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during API forwarding: {e}")

@dp.message(Command("start"))
async def handle_start(message: types.Message, bot: Bot):
    """Handles the /start command by forwarding it."""
    # Ideally we get the full Update object. We need to register a handler for Updates.
    # For now, let's just acknowledge and maybe forward basic info
    # In a real scenario, we might want the full Update context
    # await message.answer("Processing /start...") # Optional: Give user feedback
    # For simplicity now, we won't forward commands directly, we'll handle all messages
    # pass
    logging.info(f"Received /start command from chat {message.chat.id}")
    # The generic message handler below will catch this and forward the update

@dp.message(Command("help"))
async def handle_help(message: types.Message, bot: Bot):
    """Handles the /help command by forwarding it."""
    # await message.answer("Processing /help...") # Optional: Give user feedback
    # pass
    logging.info(f"Received /help command from chat {message.chat.id}")
    # The generic message handler below will catch this and forward the update

# Register a handler for *all* message types
# This will capture commands, text messages, etc.
@dp.message()
async def handle_all_messages(message: types.Message):
    """Handles all incoming messages by forwarding the update object."""
    # This handler receives the `Message` object.
    # To forward the full context, we need the `Update` object.
    # We'll adjust this by using an Update handler instead.
    pass # See the update handler below

# Correct approach: Handle the Update object directly
@dp.update()
async def handle_update(update: Update):
    """Receives all updates and forwards them to the API."""
    logging.info(f"Received update: {update.update_id}")
    await forward_to_api(update)

async def main():
    """Starts the bot polling."""
    logging.info(f"Starting bot listener... Forwarding updates to {API_BASE_URL}")
    # Start polling
    # Pass the bot instance to handlers if needed
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 