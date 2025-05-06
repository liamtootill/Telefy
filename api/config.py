import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field
from typing import Optional

logger = logging.getLogger(__name__)

# Use BaseSettings to automatically read from environment variables
# Define .env file loading if needed (optional)
# We can add validation here too

class Settings(BaseSettings):
    # Define fields corresponding to environment variables
    # Secrets (use Field(repr=False) to hide from logs/repr)
    TELEGRAM_BOT_TOKEN: str = Field(..., repr=False) 
    OPENAI_API_KEY: str = Field(..., repr=False)
    DATABASE_URL: PostgresDsn # Pydantic validates the DSN format

    # General Config
    # API_BASE_URL for listener might be better set where listener runs
    # API_BASE_URL: str = "http://localhost:8000" 
    DEFAULT_PERSONA: str = "You are a helpful AI assistant participating in a Telegram group chat."
    
    # Model Config
    LLM_MODEL: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Memory Config
    MEMORY_RETRIEVAL_LIMIT: int = 3
    MEMORY_RETRIEVAL_MAX_AGE_DAYS: int = 7
    
    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        # Load .env file if present (useful for local development)
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore' # Ignore extra env vars not defined above
    )

# Instantiate settings once
try:
    settings = Settings()
    # Log some non-sensitive settings on startup
    logger.info(f"Loaded settings: LLM_MODEL={settings.LLM_MODEL}, EMBEDDING_MODEL={settings.EMBEDDING_MODEL}")
except Exception as e:
    logger.error(f"CRITICAL: Failed to load settings. Error: {e}")
    # Application might not be able to run without settings
    settings = None # Indicate settings are unavailable

# Export the settings instance for other modules to import
# Other modules will do: from .config import settings 