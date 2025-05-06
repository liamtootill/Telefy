-- Initial database schema for the Telegram AI Agent Bot

-- Table to store information about each group chat the bot is in
CREATE TABLE IF NOT EXISTS groups (
    -- Telegram Chat ID (can be large, hence BIGINT). Primary Key.
    chat_id BIGINT PRIMARY KEY,

    -- Flag indicating if the bot is currently active in this chat
    is_active BOOLEAN NOT NULL DEFAULT true,

    -- List of Telegram User IDs allowed to administer the bot in this chat
    -- Stored as an array of big integers. Can be NULL if not restricted.
    admin_ids BIGINT[],

    -- The custom personality prompt set for this group's AI agent
    personality_prompt TEXT NULL,

    -- Timestamp when the bot first joined/was activated in this chat
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),

    -- Timestamp when the group's settings were last modified
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- Optional: Add an index on is_active if we frequently query active groups
-- CREATE INDEX IF NOT EXISTS idx_groups_is_active ON groups (is_active);

-- Trigger function to automatically update updated_at timestamp on row change
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to execute the function before any update on the groups table
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON groups
FOR EACH ROW
EXECUTE FUNCTION trigger_set_timestamp();

-- Add the new column to existing tables (if database already exists)
-- You might need to run this manually via psql or Vercel console if the table exists:
-- ALTER TABLE groups ADD COLUMN IF NOT EXISTS personality_prompt TEXT NULL;

-- ========= Chat Memory Table =========

-- Requires the pgvector extension to be enabled:
-- CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS chat_memories (
    memory_id BIGSERIAL PRIMARY KEY,
    
    -- Link to the group this memory belongs to
    chat_id BIGINT NOT NULL REFERENCES groups(chat_id) ON DELETE CASCADE,
    
    -- Original Telegram message ID (unique within a chat)
    message_id BIGINT NOT NULL,
    
    -- Telegram user ID of the message sender
    user_id BIGINT NOT NULL,
    
    -- The text content of the message
    message_text TEXT NOT NULL,
    
    -- Timestamp when the original message was sent
    message_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Embedding vector for the message text (size depends on model)
    -- For text-embedding-3-small, dimension is 1536
    embedding VECTOR(1536) NOT NULL,
    
    -- Timestamp when this memory record was created
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    
    -- Ensure messages are unique within a chat
    UNIQUE (chat_id, message_id)
);

-- Index for faster lookups by chat_id
CREATE INDEX IF NOT EXISTS idx_chat_memories_chat_id ON chat_memories (chat_id);

-- Index for vector similarity search (using HNSW algorithm with cosine distance)
-- Choose index parameters (m, ef_construction) based on dataset size and performance needs.
-- See pgvector docs for guidance. These are example values.
-- It's often recommended to build the index AFTER inserting data.
CREATE INDEX IF NOT EXISTS idx_chat_memories_embedding_hnsw ON chat_memories USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Optional: IVFFlat index example (might be better for very large datasets or different query patterns)
-- CREATE INDEX IF NOT EXISTS idx_chat_memories_embedding_ivf ON chat_memories USING ivfflat (embedding vector_cosine_ops)
-- WITH (lists = 100); -- Adjust 'lists' based on data size (sqrt(N) to N/1000)

-- Note: The persona information will be added in a later phase (e.g., in this table or a separate one).
-- Note: You need to connect to your Vercel Postgres instance and run this SQL
-- using psql or the Vercel dashboard SQL editor to create the table. 