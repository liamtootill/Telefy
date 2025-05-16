// Placeholder for Twitter mention handling logic

import { TweetV2SingleResult, TwitterApi } from 'twitter-api-v2';
import { getAgentMemory, saveAgentMemory } from '../../memory/supabaseMemory';
import { createOpenRouterClient } from '../../ai/openrouterClient';
import { systemPrompt } from '../prompts/systemPrompt';

export const handleMention = async (eventData: TweetV2SingleResult, twitterClient: TwitterApi) => {
  console.log('Twitter mention received:', eventData.data.id);
  try {
    // 1. Fetch unified agent memory
    const memory = await getAgentMemory('global_agent');
    const prompt = memory?.custom_prompt || systemPrompt;
    const model = memory?.model || 'x-ai/grok-3-mini-beta';
    const llm = createOpenRouterClient(model);
    // 2. Compose input for LLM
    const mentionText = eventData.data.text;
    const systemMessage = prompt;
    // 3. Call LLM (fix: pass a single string prompt)
    const llmPrompt = `${systemMessage}\nUser: ${mentionText}`;
    const response = await llm.invoke(llmPrompt);
    const aiReply = String(response?.content || 'Hello! I am an AI agent.');
    // 4. Reply to the tweet
    await twitterClient.v2.reply(aiReply, eventData.data.id);
    // 5. Update memory (append to summary, or use your summary logic)
    const newSummary = (memory?.summary || '') + `\nUser: ${mentionText}\nAI: ${aiReply}`;
    await saveAgentMemory('global_agent', newSummary, memory?.personality, model, memory?.custom_prompt);
    console.log('Replied to tweet.');
  } catch (e) {
    console.error('Error replying to tweet:', e);
  }
};
