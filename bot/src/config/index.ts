import dotenv from 'dotenv';

dotenv.config();

export const config = {
  telegramBotToken: process.env.TELEGRAM_BOT_TOKEN,
  openRouterApiKey: process.env.OPENROUTER_API_KEY,
  supabaseUrl: process.env.SUPABASE_URL,
  supabaseKey: process.env.SUPABASE_KEY,
  twitterBearerToken: process.env.TWITTER_BEARER_TOKEN,
};
