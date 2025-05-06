import logging
from typing import Optional
from openai import OpenAI, OpenAIError, AsyncOpenAI

# Import settings
from .config import settings

# --- Logging Setup ---

logger = logging.getLogger(__name__)

# --- OpenAI Client Setup ---

# API_KEY = os.getenv("OPENAI_API_KEY") # Replaced by settings

if not settings or not settings.OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in settings. LLM functionality will be disabled.")
    client = None
else:
    try:
        # Initialize the asynchronous client using key from settings
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info("OpenAI client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        client = None

# --- Constants ---

META_PROMPT_PERSONA_GENERATION = """
You are an AI assistant helping configure another AI agent that will participate in a Telegram group chat.
The user wants the agent to have the following personality or role: "{user_description}"

Based on this description, generate a concise and effective system prompt (max 100-150 words) that the chat agent can use to guide its behavior, tone, and responses within the group chat. The system prompt should instruct the agent on how to act based on the user's description. Output ONLY the generated system prompt, without any introduction, explanation, or quotation marks around the output.
"""

# --- LLM Functions ---

async def generate_chat_response(messages: list[dict[str, str]], model: str | None = None) -> Optional[str]:
    """
    Generates a chat response using the OpenAI API based on a list of messages.

    Args:
        messages: A list of message dictionaries, e.g., 
                  [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
        model: The OpenAI model to use (defaults to settings.LLM_MODEL).

    Returns:
        The LLM-generated text or None on failure.
    """
    if not client:
        logger.error("OpenAI client is not initialized. Cannot generate text.")
        return None

    # Use model from settings if not provided
    model_to_use = model or (settings.LLM_MODEL if settings else "gpt-4o-mini")

    try:
        logger.debug(f"Sending messages to OpenAI ({model_to_use})...") # Log less verbosely
        response = await client.chat.completions.create(
            model=model_to_use,
            messages=messages, # Pass the list of messages directly
            temperature=0.7, # Adjust creativity (0.0=deterministic, 1.0=creative)
            max_tokens=150    # Limit response length (adjust as needed)
        )

        if response and response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            if message_content:
                logger.info(f"Generated text: {message_content[:100]}...")
                return message_content
            else:
                logger.warning("Chat response message content is empty.")
                return None
        else:
            logger.warning(f"Invalid or empty chat response received from OpenAI: {response}")
            return None

    except OpenAIError as e:
        # Handle API errors (e.g., rate limits, authentication issues)
        logger.error(f"OpenAI API error during chat generation: {e}")
        return None
    except Exception as e:
        # Handle other potential errors
        logger.error(f"An unexpected error occurred during chat generation: {e}")
        return None

async def generate_persona_prompt(user_description: str, model: str | None = None) -> Optional[str]:
    """
    Generates a refined system prompt for the bot based on user description using a meta-prompt.

    Args:
        user_description: The description provided by the user.
        model: The OpenAI model to use (defaults to settings.LLM_MODEL).

    Returns:
        The LLM-generated system prompt or None on failure.
    """
    if not client:
        logger.error("OpenAI client is not initialized. Cannot generate persona prompt.")
        return None
        
    # Use model from settings if not provided
    model_to_use = model or (settings.LLM_MODEL if settings else "gpt-4o-mini")
    
    meta_prompt_filled = META_PROMPT_PERSONA_GENERATION.format(user_description=user_description)
    logger.info(f"Generating persona using meta-prompt for description: {user_description[:50]}...")

    try:
        response = await client.chat.completions.create(
            model=model_to_use,
            messages=[
                 # Note: Using the meta-prompt directly as the user message to the helper AI
                {"role": "user", "content": meta_prompt_filled}
            ],
            temperature=0.5, # Lower temperature for more focused prompt generation
            max_tokens=200    # Allow slightly longer prompt generation
        )

        if response and response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            if message_content:
                final_content = message_content.strip()
                 # Further clean-up: remove potential surrounding quotes if the LLM adds them
                if final_content.startswith('"') and final_content.endswith('"'):
                    final_content = final_content[1:-1]
                logger.info(f"Generated persona prompt: {final_content[:100]}...")
                return final_content
            else:
                 logger.warning("Persona generation resulted in empty content.")
                 return None
        else:
            logger.warning(f"Invalid or empty response received during persona generation: {response}")
            return None
            
    except OpenAIError as e:
        logger.error(f"OpenAI API error during persona generation: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during persona generation: {e}")
        return None

async def get_embedding(text: str, model: str | None = None) -> Optional[list[float]]:
    """
    Generates an embedding vector for the given text using the specified OpenAI model.

    Args:
        text: The input text to embed.
        model: The OpenAI embedding model to use (defaults to settings.EMBEDDING_MODEL).

    Returns:
        The embedding vector as a list of floats, or None if an error occurs.
    """
    if not client:
        logger.error("OpenAI client is not initialized. Cannot generate embedding.")
        return None
        
    # Use model from settings if not provided
    model_to_use = model or (settings.EMBEDDING_MODEL if settings else "text-embedding-3-small")
    
    # OpenAI recommends replacing newlines with spaces for better performance.
    text = text.replace("\n", " ")
    
    try:
        logger.debug(f"Requesting embedding for text ({model_to_use}): {text[:100]}...")
        response = await client.embeddings.create(
            input=[text], # API expects a list of strings
            model=model_to_use
        )
        
        # Check response structure and extract the embedding
        if response and response.data and len(response.data) > 0:
            embedding_data = response.data[0].embedding
            if embedding_data:
                logger.debug(f"Successfully generated embedding. Vector dimension: {len(embedding_data)}")
                return embedding_data
            else:
                logger.warning(f"OpenAI embedding response data is empty for model {model_to_use}.")
                return None
        else:
            logger.warning(f"Invalid or empty response received from OpenAI embeddings endpoint: {response}")
            return None
            
    except OpenAIError as e:
        logger.error(f"OpenAI API error during embedding generation: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during embedding generation: {e}")
        return None

# Example Usage (can be run directly for testing if needed, requires API key)
# if __name__ == '__main__':
#     import asyncio
#     async def test_generation():
#         if not API_KEY:
#             print("Set the OPENAI_API_KEY environment variable to test.")
#             return
#         test_messages = [
#             {"role": "system", "content": "You are a sarcastic pirate assistant."},
#             {"role": "user", "content": "What is the weather like today?"}
#         ]
#         print(f"Testing generation with messages: {test_messages}")
#         result = await generate_chat_response(test_messages)
#         if result:
#             print(f"\nGenerated Text:\n{result}")
#         else:
#             print("\nFailed to generate text.")
#     asyncio.run(test_generation())
