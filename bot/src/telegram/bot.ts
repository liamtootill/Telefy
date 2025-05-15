import { Telegraf } from 'telegraf';
import { message } from 'telegraf/filters';
import { config } from '../config';
import { memoryMiddleware, CustomContext } from './middleware/memoryMiddleware';
import { handleMessage } from './handlers/messageHandler';
import { handleCommand } from './handlers/commandHandler';
// import { handleCommand } from './handlers/commandHandler'; // Placeholder for future commands

if (!config.telegramBotToken) {
  throw new Error('Telegram Bot Token not configured in environment variables.');
}

// Use CustomContext for the bot instance
const bot = new Telegraf<CustomContext>(config.telegramBotToken);

// Register middleware
bot.use(memoryMiddleware);

// Register handlers
bot.command(/.*/, handleCommand); // Register for all commands
bot.on(message('text'), handleMessage);
// bot.command('somecommand', handleCommand); // Example for future command

// Basic error handler
bot.catch((err, ctx) => {
  console.error(`Ooops, encountered an error for ${ctx.updateType}`, err);
  // Optionally send a message to the chat
  // ctx.reply('Sorry, an unexpected error occurred.').catch(e => console.error('Failed to send error message to chat:', e));
});

// Start the bot
export const startTelegramBot = async () => {
  try {
    await bot.launch();
    console.log('Telegram bot started successfully!');

    // Enable graceful stop
    process.once('SIGINT', () => bot.stop('SIGINT'));
    process.once('SIGTERM', () => bot.stop('SIGTERM'));
  } catch (error) {
    console.error('Failed to start Telegram bot:', error);
    process.exit(1); // Exit if bot fails to start
  }
};
