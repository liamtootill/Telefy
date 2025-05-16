// Placeholder for Telegram command handling logic

import { CustomContext } from '../middleware/memoryMiddleware';
import { getTelegramMemory, saveTelegramMemory, getAllTelegramChatIds } from '../../memory/supabaseMemory';
import { getAgentMemory, saveAgentMemory, getAllTelegramChatIds as getAllTelegramChatIdsAgent } from '../../memory/supabaseMemory';

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
    // Only allow admin (user id 1685581595) to update prompt
    if (ctx.from?.id !== 1685581595) {
      await ctx.reply('Only the bot admin can update the prompt.');
      return;
    }
    // Get current agent memory to preserve other fields
    const memory = await getAgentMemory('global_agent');
    await saveAgentMemory(
      'global_agent',
      memory?.summary || '',
      memory?.personality,
      memory?.model,
      customPrompt
    );
    await ctx.reply('Custom prompt saved!');
    return;
  }

  // Handle /broadcast command (admin only)
  if (text.startsWith('/broadcast ')) {
    if (ctx.from?.id !== 1685581595) {
      await ctx.reply('You are not authorized to use this command.');
      return;
    }
    const broadcastMessage = text.replace('/broadcast ', '').trim();
    if (!broadcastMessage) {
      await ctx.reply('Please provide a message to broadcast.');
      return;
    }
    const chatIds = await getAllTelegramChatIdsAgent();
    let sent = 0, failed = 0;
    for (const id of chatIds) {
      try {
        await ctx.telegram.sendMessage(id, broadcastMessage);
        sent++;
        await new Promise(res => setTimeout(res, 100)); // 100ms delay
      } catch (err) {
        failed++;
      }
    }
    await ctx.reply(`Broadcast complete. Sent: ${sent}, Failed: ${failed}`);
    return;
  }

  // Example: Handle a /config command
  // const command = ctx.message.text.split(' ')[0];
  // if (command === '/config') { ... }
  return;
};
