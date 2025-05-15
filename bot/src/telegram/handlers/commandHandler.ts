// Placeholder for Telegram command handling logic

import { CustomContext } from '../middleware/memoryMiddleware';
import { getTelegramMemory, saveTelegramMemory } from '../../memory/supabaseMemory';

export const handleCommand = async (ctx: CustomContext) => {
  if (!ctx.chat || !ctx.message || !('text' in ctx.message)) {
    return;
  }
  const chatId = ctx.chat.id;
  const text = ctx.message.text.trim();

  // Handle /prompt command
  if (text.startsWith('/prompt')) {
    const customPrompt = text.replace('/prompt', '').trim();
    if (!customPrompt) {
      return;
    }
    // Check admin status in group/supergroup
    if ((ctx.chat.type === 'group' || ctx.chat.type === 'supergroup') && ctx.from) {
      const admins = await ctx.telegram.getChatAdministrators(chatId);
      const isAdmin = admins.some(a => a.user.id === ctx.from!.id && (a.status === 'administrator' || a.status === 'creator'));
      if (!isAdmin) {
        await ctx.reply('Only group admins can update the prompt.');
        return;
      }
    }
    // Get current memory to preserve other fields
    const memory = await getTelegramMemory(chatId);
    await saveTelegramMemory(
      chatId,
      memory?.summary || '',
      memory?.personality,
      memory?.model,
      customPrompt
    );
    await ctx.reply('Custom prompt saved!');
    return;
  }

  // Example: Handle a /config command
  // const command = ctx.message.text.split(' ')[0];
  // if (command === '/config') { ... }
  return;
};
