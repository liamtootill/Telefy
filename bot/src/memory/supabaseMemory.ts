import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { config } from '../config';

if (!config.supabaseUrl || !config.supabaseKey) {
  throw new Error('Supabase URL or Key not configured in environment variables.');
}

const supabase: SupabaseClient = createClient(config.supabaseUrl, config.supabaseKey);

export interface TelegramMemory {
  chat_id: number;
  summary?: string;
  personality?: string;
  model?: string;
  custom_prompt?: string;
}

export interface TwitterMemory {
  id: string; // e.g., "twitter_bot"
  memory?: string;
  personality?: string;
  model?: string;
}

export interface AgentMemory {
  id: string; // e.g., 'global_agent'
  summary?: string;
  personality?: string;
  model?: string;
  custom_prompt?: string;
}

export const getTelegramMemory = async (chatId: number): Promise<TelegramMemory | null> => {
  const { data, error } = await supabase
    .from('telegram_memories')
    .select('chat_id, summary, personality, model, custom_prompt')
    .eq('chat_id', chatId)
    .single();

  if (error && error.code !== 'PGRST116') { // PGRST116: Row not found
    console.error('Error fetching Telegram memory:', error);
    return null;
  }
  return data;
};

export const saveTelegramMemory = async (chatId: number, summary: string, personality?: string, model?: string, custom_prompt?: string): Promise<void> => {
  const { error } = await supabase
    .from('telegram_memories')
    .upsert({ chat_id: chatId, summary, personality, model, custom_prompt }, { onConflict: 'chat_id' });

  if (error) {
    console.error('Error saving Telegram memory:', error);
  }
};

export const getTwitterMemory = async (id: string = "twitter_bot"): Promise<TwitterMemory | null> => {
  const { data, error } = await supabase
    .from('twitter_memory')
    .select('*')
    .eq('id', id)
    .single();

  if (error && error.code !== 'PGRST116') {
    console.error('Error fetching Twitter memory:', error);
    return null;
  }
  return data;
};

export const saveTwitterMemory = async (id: string = "twitter_bot", memory: string, personality?: string, model?: string): Promise<void> => {
  const { error } = await supabase
    .from('twitter_memory')
    .upsert({ id, memory, personality, model }, { onConflict: 'id' });

  if (error) {
    console.error('Error saving Twitter memory:', error);
  }
};

export const getAllTelegramChatIds = async (): Promise<number[]> => {
  const { data, error } = await supabase
    .from('telegram_memories')
    .select('chat_id');
  if (error) {
    console.error('Error fetching chat IDs:', error);
    return [];
  }
  return (data || []).map((row: { chat_id: number }) => row.chat_id);
};

export const getAgentMemory = async (id: string = 'global_agent'): Promise<AgentMemory | null> => {
  const { data, error } = await supabase
    .from('agent_memories')
    .select('*')
    .eq('id', id)
    .single();

  if (error && error.code !== 'PGRST116') {
    console.error('Error fetching agent memory:', error);
    return null;
  }
  return data;
};

export const saveAgentMemory = async (
  id: string = 'global_agent',
  summary?: string,
  personality?: string,
  model?: string,
  custom_prompt?: string
): Promise<void> => {
  const { error } = await supabase
    .from('agent_memories')
    .upsert({ id, summary, personality, model, custom_prompt }, { onConflict: 'id' });

  if (error) {
    console.error('Error saving agent memory:', error);
  }
};
