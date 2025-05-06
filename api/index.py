# Placeholder for FastAPI application logic
# This will run as a Vercel Serverless Function

import logging
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel # For request body validation
from typing import Any, Dict # For flexible Update structure
from contextlib import asynccontextmanager # For lifespan management
from datetime import datetime # Added for timestamp conversion
import os

# Import database utility functions
import database # Adjusted import for api/ structure
# Import LLM service functions
import llm_service # Added import for LLM
# Import Telegram utility functions
import telegram_utils # Added import for sending messages
# Import settings
from .config import settings

# Configure basic logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# --- Configuration --- 
# Now handled by config.py, remove direct os.getenv calls here
# try:
#     MEMORY_RETRIEVAL_LIMIT = int(os.getenv("MEMORY_RETRIEVAL_LIMIT", "3"))
# ... (removed block) ...
# except ValueError:
#     logger.warning("Invalid MEMORY_RETRIEVAL_MAX_AGE_DAYS env var. Using default: 7")
#     MEMORY_RETRIEVAL_MAX_AGE_DAYS = 7
# --- End Configuration --- 

# Use FastAPI's lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    logger.info("Application startup: Initializing database pool...")
    await database.init_db_pool()
    logger.info("Fetching bot info (username and ID)...")
    # Fetch and cache the bot info on startup
    await telegram_utils.fetch_bot_info()
    if not telegram_utils.BOT_USERNAME or not telegram_utils.BOT_USER_ID:
        logger.error("CRITICAL: Failed to fetch bot username or ID on startup. Triggering logic might be impaired.")
        # Decide if the app should fail to start or continue with degraded functionality
    yield # The application runs while yielding
    # Code to run on shutdown
    logger.info("Application shutdown: Closing database pool...")
    await database.close_db_pool()

app = FastAPI(lifespan=lifespan)

# Pydantic model for the incoming Telegram Update
# We use Dict[str, Any] for flexibility as the Update structure is complex
# and aiogram's models aren't directly used here.
class TelegramUpdate(BaseModel):
    update_id: int
    message: Dict[str, Any] | None = None
    edited_message: Dict[str, Any] | None = None
    channel_post: Dict[str, Any] | None = None
    edited_channel_post: Dict[str, Any] | None = None
    # Add other potential update types as needed (inline_query, chosen_inline_result, etc.)
    # Use Dict[str, Any] or more specific Pydantic models if needed


@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI - Bot API Endpoint"}

@app.post("/api/webhook")
async def telegram_webhook(update: TelegramUpdate):
    """Handles incoming updates forwarded from the listener."""
    logger.info(f"Received update via webhook: {update.update_id}")

    # 1. Handle non-message updates early
    if update.edited_message:
        chat_id = update.edited_message.get('chat', {}).get('id', 'N/A')
        msg_id = update.edited_message.get('message_id', 'N/A')
        logger.info(f"Received edited message {msg_id} in chat {chat_id}. Ignoring.")
        return {"status": "ok", "detail": "Edited message ignored"}
    if update.channel_post:
        logger.info(f"Received channel post {update.channel_post.get('message_id', 'N/A')}. Ignoring.")
        return {"status": "ok", "detail": "Channel post ignored"}
    if not update.message:
        logger.info(f"Received non-message update type. Ignoring.")
        return {"status": "ok", "detail": "Unsupported update type ignored"}

    # 2. Process the message
    message_data = update.message
    chat_id = message_data.get('chat', {}).get('id')
    message_text = message_data.get('text') # Can be None

    # 3. Validate essential data
    if not chat_id:
        logger.error(f"Could not extract chat ID from message. Update: {update.model_dump_json(exclude_none=True)}")
        return {"status": "error", "detail": "Missing chat ID"}

    # 4. Ensure group exists in DB
    group_record = await database.get_or_create_group(chat_id)
    if not group_record:
        logger.error(f"Failed to get or create group {chat_id}. Skipping.")
        return {"status": "error", "detail": "Database group operation failed"}
    # Optional: Check if group is active: if not group_record['is_active']: return {"status": "ok", "detail": "Bot inactive in group"}

    # 5. Handle non-text messages
    if not message_text:
        logger.info(f"Received non-text message in chat {chat_id}. Ignoring.")
        return {"status": "ok", "detail": "Non-text message ignored"}
    # --- End Task 5.5 Handling ---

    logger.info(f"Processing text message in Chat ID: {chat_id} - Message: {message_text[:50]}...")
    sender_user_id = message_data.get('from', {}).get('id')

    # 6. Handle Commands
    if message_text.startswith('/'):
        command = message_text.split()[0]
        logger.debug(f"Detected command: {command}")

        # === /start ===
        if command == '/start':
            # TODO: /start logic
            await telegram_utils.send_telegram_message(chat_id=chat_id, text="Hello! I'm your friendly AI agent. Use /help to see what I can do.")
            return {"status": "ok", "detail": "Command processed"}

        # === /help ===
        elif command == '/help':
            # TODO: /help logic
            help_text = """
Available commands:
/help - Show this help message
/set_personality <description> - Set my personality (admins only)
/get_personality - View my current personality
/add_admin <user_id> - Add a bot admin (admins only)
/remove_admin <user_id> - Remove a bot admin (admins only)
/list_admins - List current bot admins (admins only)
            """
            await telegram_utils.send_telegram_message(chat_id=chat_id, text=help_text)
            return {"status": "ok", "detail": "Command processed"}

        # === /set_personality ===
        elif command == '/set_personality':
            command_parts = message_text.split(maxsplit=1)
            if len(command_parts) < 2 or not command_parts[1].strip():
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Usage: /set_personality <description>")
                return {"status": "ok", "detail": "Prompt missing"}
            new_prompt_desc = command_parts[1].strip()

            if not sender_user_id: 
                logger.error(f"Could not identify sender for /set_personality in chat {chat_id}")
                return {"status": "error", "detail": "Could not identify sender"}

            current_admins = await database.get_group_admins(chat_id)
            if not current_admins or sender_user_id not in current_admins:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Sorry, only admins can set the personality.")
                return {"status": "ok", "detail": "Unauthorized"}

            logger.info(f"Generating persona prompt for chat {chat_id}...")
            generated_prompt = await llm_service.generate_persona_prompt(user_description=new_prompt_desc)
            if not generated_prompt:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Error: Could not generate personality prompt.")
                # Return ok because the command was handled, even if unsuccessfully
                return {"status": "ok", "detail": "LLM generation failed"} 

            success = await database.set_group_personality(chat_id, generated_prompt)
            if success:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Personality prompt generated and set!")
            else:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Error: Could not save personality.")
            return {"status": "ok", "detail": "Command processed"}

        # === /get_personality ===
        elif command == '/get_personality':
            logger.info("Processing /get_personality command")
            current_prompt = await database.get_group_personality(chat_id)
            if current_prompt:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text=f"Current personality prompt:\n\n{current_prompt}")
            else:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="No custom personality set.")
            return {"status": "ok", "detail": "Command processed"}

        # === /add_admin ===
        elif command == '/add_admin':
            logger.info("Processing /add_admin command")
            command_parts = message_text.split(maxsplit=1)
            if len(command_parts) < 2:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="Usage: /add_admin <user_id>")
                 return {"status": "ok", "detail": "Missing user ID"}
            try: target_user_id = int(command_parts[1])
            except ValueError:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="Invalid user ID.")
                 return {"status": "ok", "detail": "Invalid user ID"}

            if not sender_user_id: 
                logger.error(f"Could not identify sender for /add_admin in chat {chat_id}")
                return {"status": "error", "detail": "Could not identify sender"}

            current_admins = await database.get_group_admins(chat_id)
            is_authorized = False
            if not current_admins: # First admin must add self
                if sender_user_id == target_user_id: is_authorized = True
                else:
                    await telegram_utils.send_telegram_message(chat_id=chat_id, text="No admins set. First admin must add themselves.")
                    return {"status": "ok", "detail": "Unauthorized - first admin must self-add"}
            elif sender_user_id in current_admins: is_authorized = True

            if not is_authorized:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="You are not authorized to add admins.")
                 return {"status": "ok", "detail": "Unauthorized"}

            success = await database.add_group_admin(chat_id, target_user_id)
            await telegram_utils.send_telegram_message(chat_id=chat_id, text=f"User {target_user_id} {'added as admin.' if success else 'could not be added (maybe already admin?).'}")
            return {"status": "ok", "detail": "Command processed"}

        # === /remove_admin ===
        elif command == '/remove_admin':
            logger.info("Processing /remove_admin command")
            command_parts = message_text.split(maxsplit=1)
            if len(command_parts) < 2:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="Usage: /remove_admin <user_id>")
                 return {"status": "ok", "detail": "Missing user ID"}
            try: target_user_id = int(command_parts[1])
            except ValueError:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="Invalid user ID.")
                 return {"status": "ok", "detail": "Invalid user ID"}

            if not sender_user_id: 
                logger.error(f"Could not identify sender for /remove_admin in chat {chat_id}")
                return {"status": "error", "detail": "Could not identify sender"}

            current_admins = await database.get_group_admins(chat_id)
            if not current_admins or sender_user_id not in current_admins:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="You are not authorized to remove admins.")
                 return {"status": "ok", "detail": "Unauthorized"}
            if len(current_admins) == 1 and current_admins[0] == target_user_id:
                await telegram_utils.send_telegram_message(chat_id=chat_id, text="Cannot remove the last admin.")
                return {"status": "ok", "detail": "Cannot remove last admin"}

            success = await database.remove_group_admin(chat_id, target_user_id)
            await telegram_utils.send_telegram_message(chat_id=chat_id, text=f"User {target_user_id} {'removed from admins.' if success else 'could not be removed (maybe not an admin?).'}")
            return {"status": "ok", "detail": "Command processed"}

        # === /list_admins ===
        elif command == '/list_admins':
            logger.info("Processing /list_admins command")
            if not sender_user_id: 
                 logger.error(f"Could not identify sender for /list_admins in chat {chat_id}")
                 return {"status": "error", "detail": "Could not identify sender"}
                 
            current_admins = await database.get_group_admins(chat_id)
            # Restrict listing to admins
            if not current_admins or sender_user_id not in current_admins:
                 await telegram_utils.send_telegram_message(chat_id=chat_id, text="You must be an admin to list admins.")
                 return {"status": "ok", "detail": "Unauthorized"}

            admin_list_str = "\n".join(map(str, current_admins)) if current_admins else "None"
            await telegram_utils.send_telegram_message(chat_id=chat_id, text=f"Current Admins:\n{admin_list_str}")
            return {"status": "ok", "detail": "Command processed"}

        # === Unrecognized Command ===
        else:
            logger.info(f"Received unrecognized command: {command}")
            await telegram_utils.send_telegram_message(chat_id=chat_id, text="Sorry, I don't recognize that command. Use /help.")
            return {"status": "ok", "detail": "Unrecognized command"}

    # 7. Handle Non-Command Messages
    else:
        logger.debug("Processing as non-command message")

        # Trigger Check
        # Use settings if available, otherwise None
        bot_username = telegram_utils.BOT_USERNAME # Still relies on global cache from fetch_bot_info
        bot_user_id = telegram_utils.BOT_USER_ID   # Still relies on global cache from fetch_bot_info
        
        is_mention = bot_username and bot_username in message_text
        is_reply_to_bot = False
        reply_info = message_data.get('reply_to_message')
        if reply_info and bot_user_id and reply_info.get('from', {}).get('id') == bot_user_id:
            is_reply_to_bot = True

        if not (is_mention or is_reply_to_bot):
            logger.debug(f"Ignoring message in chat {chat_id} (Not mention or reply to bot).")
            return {"status": "ok", "detail": "Message ignored (no trigger)"}

        # Triggered: Proceed with RAG
        logger.info(f"Bot trigger detected (Mention: {is_mention}, Reply: {is_reply_to_bot}). Proceeding...")

        # Get Persona
        persona_prompt = await database.get_group_personality(chat_id) or settings.DEFAULT_PERSONA
        logger.debug(f"Using persona: {persona_prompt[:50]}...")

        # Embed/Store Incoming Message
        embedding = None
        message_id = message_data.get('message_id')
        message_dt_unix = message_data.get('date')
        if message_id and sender_user_id and message_dt_unix:
            try:
                message_dt = datetime.fromtimestamp(message_dt_unix)
                logger.debug(f"Generating embedding for message {message_id}...")
                embedding = await llm_service.get_embedding(text=message_text)
                if embedding:
                    logger.debug(f"Storing message {message_id} and embedding to memory.")
                    await database.add_chat_memory(
                        chat_id=chat_id, message_id=message_id, user_id=sender_user_id,
                        message_text=message_text, message_timestamp=message_dt, embedding=embedding
                    )
                else: logger.warning(f"Could not generate embedding for message {message_id}.")
            except Exception as e:
                 logger.error(f"Error processing incoming message for memory: {e}")
                 embedding = None # Ensure embedding is None if error
        else:
             logger.warning(f"Missing data for memory storage: msg_id={message_id}, sender={sender_user_id}, ts={message_dt_unix}")

        # Retrieve Memories
        relevant_memories = []
        if embedding:
            logger.debug(f"Finding relevant memories...")
            relevant_memories = await database.find_relevant_memories(
                chat_id=chat_id, query_embedding=embedding,
                limit=settings.MEMORY_RETRIEVAL_LIMIT, 
                max_age_days=settings.MEMORY_RETRIEVAL_MAX_AGE_DAYS
            )
            logger.info(f"Found {len(relevant_memories)} relevant memories (limit={settings.MEMORY_RETRIEVAL_LIMIT}, max_age={settings.MEMORY_RETRIEVAL_MAX_AGE_DAYS} days).")
        else:
            logger.warning(f"Skipping memory retrieval because query embedding is missing.")

        # Build Prompt
        llm_messages = [{"role": "system", "content": persona_prompt}]
        if relevant_memories:
            context_header = "Relevant past messages (most relevant first):\n---"
            llm_messages.append({"role": "system", "content": context_header})
            bot_user_id_local = telegram_utils.BOT_USER_ID
            for memory in relevant_memories:
                 mem_ts_str = memory['message_timestamp'].strftime("%Y-%m-%d %H:%M")
                 mem_user_id = memory['user_id']
                 mem_text = memory['message_text']
                 speaker = f"User {mem_user_id}"
                 if bot_user_id_local and mem_user_id == bot_user_id_local: speaker = "You (the bot)"
                 max_len = 150
                 if len(mem_text) > max_len: mem_text = mem_text[:max_len] + "..."
                 formatted_mem = f"{speaker} previously said at {mem_ts_str}: {mem_text}"
                 llm_messages.append({"role": "system", "content": formatted_mem})
            llm_messages.append({"role": "system", "content": "---\nRespond to the current user message:"})
        llm_messages.append({"role": "user", "content": message_text})
        logger.debug(f"Constructed LLM messages (RAG): Count={len(llm_messages)}")

        # Call LLM
        bot_response_text = await llm_service.generate_chat_response(messages=llm_messages)

        # Send Response & Store Bot Message
        if bot_response_text:
            send_result = await telegram_utils.send_telegram_message(chat_id=chat_id, text=bot_response_text)
            if send_result.get("success"):
                bot_msg_id = send_result.get("message_id")
                bot_user_id_to_store = telegram_utils.BOT_USER_ID
                if bot_msg_id and bot_user_id_to_store:
                    bot_msg_dt = datetime.now()
                    logger.debug(f"Storing bot response (msg_id: {bot_msg_id}) to memory...")                    
                    bot_embedding = await llm_service.get_embedding(text=bot_response_text)
                    if bot_embedding:
                         await database.add_chat_memory(
                             chat_id=chat_id, message_id=bot_msg_id, user_id=bot_user_id_to_store,
                             message_text=bot_response_text, message_timestamp=bot_msg_dt, embedding=bot_embedding
                         )
                         logger.info(f"Stored bot response (msg_id: {bot_msg_id}) to memory.")
                    else: logger.warning(f"Could not generate embedding for bot response.")
                else: logger.warning(f"Could not store bot response: Missing bot msg ID or user ID.")
            else: # Failed to send
                logger.error(f"Failed to send bot response message to chat {chat_id}.")
        else: # Failed to generate
            logger.error(f"LLM failed to generate response for chat {chat_id}.")
            await telegram_utils.send_telegram_message(chat_id=chat_id, text="Sorry, error generating response.")

        # End of triggered non-command message handling
        return {"status": "ok"}

    # This final return should only be reached if something unexpected happens,
    # as all paths (command, triggered non-command, ignored non-command) should return earlier.
    logger.warning("Reached end of webhook handler unexpectedly.") 
    return {"status": "ok"}

# More endpoints will be added here to handle specific bot functionalities if needed

# Note: For Vercel deployment, you might need a vercel.json configuration
# to map this FastAPI app correctly. 