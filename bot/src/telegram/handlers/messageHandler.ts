import { message } from 'telegraf/filters';
import { CustomContext } from '../middleware/memoryMiddleware';
import { AIMessage, HumanMessage, SystemMessage, BaseMessage } from "@langchain/core/messages";
import { DuckDuckGoSearch } from "@langchain/community/tools/duckduckgo_search";
import { AgentExecutor, createReactAgent } from "langchain/agents";
import { pull } from "langchain/hub";
import { PromptTemplate } from "@langchain/core/prompts";

// Limit conversation history length (e.g., last 10 exchanges)
const MAX_HISTORY_LENGTH = 20; // 10 user + 10 assistant messages

const trimHistory = (history: string): string => {
  const lines = history.split('\n');
  if (lines.length > MAX_HISTORY_LENGTH) {
    return lines.slice(-MAX_HISTORY_LENGTH).join('\n');
  }
  return history;
};

// Function to parse history string into message objects
const parseHistory = (history: string): BaseMessage[] => {
  const messages: BaseMessage[] = [];
  const lines = history.trim().split('\n');
  for (const line of lines) {
    if (line.startsWith('User:')) {
      messages.push(new HumanMessage(line.replace('User: ', '')));
    } else if (line.startsWith('AI:')) {
      messages.push(new AIMessage(line.replace('AI: ', '')));
    }
  }
  return messages;
};

// --- Rate Limiting ---
const RATE_LIMIT_WINDOW_MS = 10_000; // 10 seconds
const RATE_LIMIT_MAX = 3; // max responses per window
const rateLimitMap = new Map<number, number[]>(); // chatId -> [timestamps]

export const handleMessage = async (ctx: CustomContext) => {
  // --- Initial Checks & Context --- 
  if (!ctx.chat) {
    console.warn('Skipping message: Chat context not found');
    return;
  }
  const chatId = ctx.chat.id;
  const chatType = ctx.chat.type;

  // --- Rate Limiting ---
  const now = Date.now();
  const timestamps = rateLimitMap.get(chatId) || [];
  const recent = timestamps.filter(ts => now - ts < RATE_LIMIT_WINDOW_MS);
  if (recent.length >= RATE_LIMIT_MAX) {
    await ctx.reply('Rate limit exceeded. Please wait before sending more messages.', { reply_parameters: ctx?.message?.message_id ? { message_id: ctx?.message?.message_id } : undefined });
    return;
  }
  recent.push(now);
  rateLimitMap.set(chatId, recent);

  if (!ctx.message || !('text' in ctx.message) || !ctx.state.llm || !ctx.state.personality || !ctx.botInfo) {
    console.warn('Skipping message: Invalid context, message type, or bot info missing');
    return;
  }
  const userMessageText = ctx.message.text;
  // Ignore commands (messages starting with '/')
  if (userMessageText.startsWith('/')) {
    return;
  }
  const llm = ctx.state.llm;
  const conversationHistoryString = ctx.state.conversationHistory || '';
  const personality = ctx.state.personality;
  const customPrompt = ctx.state.memoryData?.custom_prompt || '';
  const systemPrompt = `${personality}${customPrompt ? '\n' + customPrompt : ''}`;
  const botUsername = ctx.botInfo.username;
  const botId = ctx.botInfo.id;

  // --- Response Trigger Logic --- 
  let shouldRespond = false;

  if (chatType === 'private') {
    shouldRespond = true; // Always respond in private chats
  } else if (chatType === 'group' || chatType === 'supergroup') {
    // Check for mention
    if (userMessageText.includes(`@${botUsername}`)) {
      shouldRespond = true;
    }
    // Check for reply to bot
    if (ctx.message.reply_to_message && ctx.message.reply_to_message.from?.id === botId) {
      shouldRespond = true;
    }
  }

  if (!shouldRespond) {
    console.log(`[Chat ${chatId} (${chatType})] Skipping message: No trigger condition met.`);
    return; // Don't process if conditions aren't met
  }

  // --- Process Message with Agent --- 
  console.log(`[Chat ${chatId} (${chatType})] Triggered. Received: ${userMessageText}`);

  try {
    await ctx.telegram.sendChatAction(chatId, 'typing');

    // 1. Define Tools
    const tools = [new DuckDuckGoSearch({ maxResults: 3 })]; // Simple search tool

    // 2. Create Agent Prompt (Using a standard ReAct prompt from Langchain Hub)
    // Ensures the agent knows how to use tools and format its thoughts/actions
    const prompt = await pull<PromptTemplate>("hwchase17/react-chat");

    // 3. Create Agent
    const agent = await createReactAgent({
      llm,
      tools,
      prompt,
    });

    // 4. Define Error Handler for Tools
    const handleToolError = (error: any) => {
      console.error(`[Chat ${chatId}] Tool Error:`, error);
      // Instruct the agent that the search failed and it should proceed without it.
      return "Search tool failed. Proceeding with internal knowledge.";
    };

    // 5. Create Agent Executor with Error Handling
    const agentExecutor = new AgentExecutor({
      agent,
      tools,
      handleParsingErrors: handleToolError, // Use handleParsingErrors
      // verbose: true, // Uncomment for debugging agent steps
    });

    // 6. Parse History for Agent
    const historyMessages = parseHistory(conversationHistoryString);

    // 7. Invoke Agent Executor
    // Note: We include the personality/system message within the history for the agent
    const agentInput = {
        input: userMessageText,
        chat_history: [
            new SystemMessage(systemPrompt), // Use combined prompt
            ...historyMessages
        ]
    };
    // console.log(`[Chat ${chatId}] Sending to Agent:`, JSON.stringify(agentInput, null, 2));
    const agentResponse = await agentExecutor.invoke(agentInput);
    
    // Agent response usually has an 'output' field
    const aiResponseText = agentResponse.output || "Sorry, I couldn't process that.";

    console.log(`[Chat ${chatId}] AI Agent Output: ${aiResponseText}`);

    // 8. Update History (using original user text and final AI output)
    const newHistory = `${conversationHistoryString}
User: ${userMessageText}
AI: ${aiResponseText}`;
    ctx.state.conversationHistory = trimHistory(newHistory);

    // 9. Reply to User
    await ctx.reply(aiResponseText, { reply_parameters: { message_id: ctx.message.message_id }});

  } catch (error) {
    console.error(`[Chat ${chatId}] Error processing message with agent:`, error);
    await ctx.reply('Sorry, I encountered an error processing your message.', { reply_parameters: { message_id: ctx.message.message_id }});
  }
};
