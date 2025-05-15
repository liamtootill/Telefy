import { startTelegramBot } from './telegram/bot';
import { startTwitterBot } from './twitter/twitterBot';

console.log('Starting AI Agent...');

// Start Telegram Bot
startTelegramBot();

// Start Twitter Bot (if configured)
// startTwitterBot();

console.log('AI Agent initialized.'); 