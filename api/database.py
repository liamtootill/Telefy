import asyncpg
import logging
import os
from typing import Optional, List
from datetime import datetime

# Import settings
from .config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DATABASE_URL = os.getenv("DATABASE_URL") # Replaced by settings
# if not DATABASE_URL:
#     logger.error("DATABASE_URL environment variable not set.")
#     # raise ValueError("DATABASE_URL environment variable not set.")

# Global variable to hold the connection pool
# It will be initialized in the main app startup
pool: Optional[asyncpg.Pool] = None

async def init_db_pool():
    """Initializes the database connection pool."""
    global pool
    if not settings or not settings.DATABASE_URL:
        logger.error("Cannot initialize DB pool because DATABASE_URL is not set in settings.")
        return # Or raise an error

    try:
        # Convert Pydantic PostgresDsn back to string for asyncpg
        db_url_str = str(settings.DATABASE_URL)
        pool = await asyncpg.create_pool(
            db_url_str,
            min_size=1, # Minimum number of connections in the pool
            max_size=10 # Maximum number of connections in the pool
        )
        logger.info("Database connection pool created successfully.")
        # Optional: Test connection
        async with pool.acquire() as connection:
            val = await connection.fetchval('SELECT 1')
            if val == 1:
                logger.info("Database connection test successful.")
            else:
                logger.warning("Database connection test returned unexpected value.")
    except Exception as e:
        logger.error(f"Failed to create database connection pool: {e}")
        pool = None # Ensure pool is None if initialization fails

async def close_db_pool():
    """Closes the database connection pool."""
    global pool
    if pool:
        try:
            await pool.close()
            logger.info("Database connection pool closed.")
        except Exception as e:
            logger.error(f"Error closing database connection pool: {e}")
        finally:
            pool = None


async def get_or_create_group(chat_id: int) -> Optional[asyncpg.Record]:
    """
    Retrieves group details from the database by chat_id.
    If the group doesn't exist, it creates a new entry.
    Returns the group record or None if an error occurs or pool is not initialized.
    """
    if not pool:
        logger.error("Database pool is not initialized.")
        return None

    async with pool.acquire() as connection:
        async with connection.transaction():
            # Attempt to fetch the group first
            group_record = await connection.fetchrow(
                "SELECT chat_id, is_active, admin_ids, created_at, updated_at FROM groups WHERE chat_id = $1",
                chat_id
            )

            if group_record:
                logger.debug(f"Group {chat_id} found in database.")
                return group_record
            else:
                # Group not found, create it
                logger.info(f"Group {chat_id} not found. Creating new entry.")
                try:
                    # Insert the new group with default values
                    # admin_ids is left NULL initially
                    new_group_record = await connection.fetchrow(
                        """
                        INSERT INTO groups (chat_id)
                        VALUES ($1)
                        RETURNING chat_id, is_active, admin_ids, created_at, updated_at
                        """,
                        chat_id
                    )
                    logger.info(f"Group {chat_id} created successfully.")
                    return new_group_record
                except asyncpg.UniqueViolationError:
                    # Highly unlikely race condition: another process inserted between SELECT and INSERT
                    logger.warning(f"Race condition: Group {chat_id} was created concurrently. Fetching again.")
                    # Fetch the concurrently inserted record
                    group_record = await connection.fetchrow(
                        "SELECT chat_id, is_active, admin_ids, created_at, updated_at FROM groups WHERE chat_id = $1",
                        chat_id
                    )
                    return group_record
                except Exception as e:
                    logger.error(f"Error creating group {chat_id}: {e}")
                    # Re-raise the exception to potentially roll back the transaction if needed elsewhere
                    # raise e
                    return None

# Example of an update function (we might need this later)
async def set_group_activity(chat_id: int, is_active: bool) -> bool:
    """Sets the activity status for a given group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return False

    try:
        async with pool.acquire() as connection:
            result = await connection.execute(
                "UPDATE groups SET is_active = $1 WHERE chat_id = $2",
                is_active, chat_id
            )
            # result format is like 'UPDATE N' where N is rows affected
            rows_affected = int(result.split()[-1])
            if rows_affected > 0:
                logger.info(f"Set group {chat_id} active status to {is_active}")
                return True
            else:
                logger.warning(f"Attempted to update activity for non-existent group {chat_id}")
                return False
    except Exception as e:
        logger.error(f"Error updating group {chat_id} activity: {e}")
        return False

async def get_group_admins(chat_id: int) -> Optional[List[int]]:
    """Retrieves the list of admin user IDs for a given group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return None
    try:
        async with pool.acquire() as connection:
            # Fetch only the admin_ids column
            admin_ids = await connection.fetchval(
                "SELECT admin_ids FROM groups WHERE chat_id = $1",
                chat_id
            )
            # fetchval returns None if the record doesn't exist or admin_ids is NULL
            # It returns a list directly if the column type is an array (like BIGINT[])
            logger.debug(f"Fetched admin_ids for chat {chat_id}: {admin_ids}")
            return admin_ids # This will be None or a list[int]
    except Exception as e:
        logger.error(f"Error fetching admin IDs for group {chat_id}: {e}")
        return None

async def set_group_personality(chat_id: int, personality_prompt: str) -> bool:
    """Sets the personality prompt for a given group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return False

    try:
        async with pool.acquire() as connection:
            result = await connection.execute(
                "UPDATE groups SET personality_prompt = $1 WHERE chat_id = $2",
                personality_prompt, chat_id
            )
            # result format is like 'UPDATE N' where N is rows affected
            rows_affected = int(result.split()[-1])
            if rows_affected > 0:
                logger.info(f"Set personality for group {chat_id}")
                return True
            else:
                # This case means the group didn't exist in the table.
                # get_or_create_group should have been called first, but handle defensively.
                logger.warning(f"Attempted to set personality for non-existent group {chat_id}")
                return False
    except Exception as e:
        logger.error(f"Error setting personality for group {chat_id}: {e}")
        return False

async def get_group_personality(chat_id: int) -> Optional[str]:
    """Retrieves the currently set personality prompt for a given group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return None
    try:
        async with pool.acquire() as connection:
            # Fetch the personality_prompt column
            # fetchval returns the value of the first column of the first row, or None
            personality = await connection.fetchval(
                "SELECT personality_prompt FROM groups WHERE chat_id = $1",
                chat_id
            )
            if personality is not None:
                 logger.debug(f"Fetched personality for chat {chat_id}: {personality[:50]}...")
            else:
                 # This can happen if the group exists but prompt is NULL, or if group doesn't exist
                 logger.debug(f"No personality prompt found for chat {chat_id} (might be NULL or group non-existent).")
            return personality # Returns the string or None
    except Exception as e:
        logger.error(f"Error fetching personality for group {chat_id}: {e}")
        return None

async def add_chat_memory(
    chat_id: int,
    message_id: int,
    user_id: int,
    message_text: str,
    message_timestamp: datetime,
    embedding: List[float]
) -> bool:
    """Adds a message and its embedding to the chat_memories table."""
    if not pool:
        logger.error("Database pool is not initialized. Cannot add memory.")
        return False

    if not embedding:
        logger.error(f"Attempted to add memory for msg {message_id} in chat {chat_id} with empty embedding.")
        return False
        
    try:
        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO chat_memories 
                    (chat_id, message_id, user_id, message_text, message_timestamp, embedding)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (chat_id, message_id) DO NOTHING; -- Ignore if message already exists
                """,
                chat_id,
                message_id,
                user_id,
                message_text,
                message_timestamp,
                embedding # asyncpg handles list[float] conversion to vector
            )
            logger.info(f"Successfully added/ignored memory for msg {message_id} in chat {chat_id}.")
            return True
    except asyncpg.exceptions.UndefinedFunctionError as e:
         # This likely means the vector extension isn't properly enabled/installed
         logger.error(f"Database error adding chat memory: Vector function undefined. Is pgvector enabled? Details: {e}")
         return False
    except Exception as e:
        logger.error(f"Unexpected error adding chat memory for msg {message_id} in chat {chat_id}: {e}")
        return False

async def find_relevant_memories(
    chat_id: int, 
    query_embedding: List[float], 
    limit: int = 3,
    max_age_days: Optional[int] = 7 # Default to only considering memories from last 7 days
) -> List[asyncpg.Record]:
    """Finds relevant chat memories using vector similarity search.
    Optionally filters memories by age.
    """
    if not pool:
        logger.error("Database pool is not initialized. Cannot find memories.")
        return []
    
    if not query_embedding:
        logger.error(f"Attempted to find memories in chat {chat_id} with empty query embedding.")
        return []

    try:
        async with pool.acquire() as connection:
            # Base query + parameters
            sql_query = """
                SELECT memory_id, message_text, user_id, message_timestamp 
                FROM chat_memories 
                WHERE chat_id = $1 
            """
            params = [chat_id]
            param_index = 2 # Start index for next parameters

            # Add time-based filtering if requested
            if max_age_days is not None and max_age_days > 0:
                 sql_query += f" AND message_timestamp >= NOW() - INTERVAL '${param_index} day' "
                 params.append(max_age_days)
                 param_index += 1
                 logger.debug(f"Filtering memories to last {max_age_days} days.")

            # Add vector search condition
            sql_query += f" ORDER BY embedding <=> ${param_index} " # Cosine distance
            params.append(query_embedding)
            param_index += 1

            # Add limit
            sql_query += f" LIMIT ${param_index}; "
            params.append(limit)

            logger.debug(f"Executing memory search query: {sql_query} with params: {params[:1] + ['<embedding>'] + params[2:]}")

            memories = await connection.fetch(sql_query, *params)
            
            logger.info(f"Retrieved {len(memories)} relevant memories for chat {chat_id} (limit {limit}, max_age {max_age_days} days).")
            return memories
    except asyncpg.exceptions.UndefinedFunctionError as e:
         logger.error(f"Database error finding memories: Vector operator/function undefined. Is pgvector enabled? Details: {e}")
         return []
    except Exception as e:
        logger.error(f"Unexpected error finding relevant memories for chat {chat_id}: {e}")
        return [] 

async def add_group_admin(chat_id: int, user_id_to_add: int) -> bool:
    """Adds a user ID to the admin_ids array for a group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return False
    try:
        async with pool.acquire() as connection:
            # Use COALESCE to handle NULL admin_ids, append if not already present
            result = await connection.execute(
                """ 
                UPDATE groups 
                SET admin_ids = array_append(COALESCE(admin_ids, ARRAY[]::BIGINT[]), $1) 
                WHERE chat_id = $2 AND (admin_ids IS NULL OR NOT admin_ids @> ARRAY[$1]::BIGINT[]);
                """,
                user_id_to_add,
                chat_id
            )
            rows_affected = int(result.split()[-1])
            if rows_affected > 0:
                logger.info(f"Added user {user_id_to_add} to admins for chat {chat_id}.")
                return True
            else:
                # Could mean group doesn't exist OR user was already an admin
                # Check if user is already admin to confirm
                current_admins = await get_group_admins(chat_id)
                if current_admins and user_id_to_add in current_admins:
                     logger.info(f"User {user_id_to_add} was already an admin for chat {chat_id}. No change needed.")
                     return True # Indicate success as the user is an admin
                else:
                     logger.warning(f"Failed to add admin {user_id_to_add} for chat {chat_id}. Group not found or user already exists?")
                     return False
    except Exception as e:
        logger.error(f"Error adding admin {user_id_to_add} for chat {chat_id}: {e}")
        return False

async def remove_group_admin(chat_id: int, user_id_to_remove: int) -> bool:
    """Removes a user ID from the admin_ids array for a group."""
    if not pool:
        logger.error("Database pool is not initialized.")
        return False
    try:
        async with pool.acquire() as connection:
            # Use array_remove. This works even if admin_ids is NULL or user is not present.
            result = await connection.execute(
                """
                UPDATE groups 
                SET admin_ids = array_remove(admin_ids, $1) 
                WHERE chat_id = $2;
                """,
                user_id_to_remove,
                chat_id
            )
            rows_affected = int(result.split()[-1]) # Will be 1 if group exists, 0 otherwise
            if rows_affected > 0:
                 logger.info(f"Removed user {user_id_to_remove} from admins for chat {chat_id} (if they were present)." )
                 return True
            else:
                 logger.warning(f"Attempted to remove admin {user_id_to_remove} for non-existent group {chat_id}.")
                 return False # Group likely didn't exist
    except Exception as e:
        logger.error(f"Error removing admin {user_id_to_remove} for chat {chat_id}: {e}")
        return False