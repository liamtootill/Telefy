import { ChatOpenAI } from "@langchain/openai";
import { config } from '../config';

if (!config.openRouterApiKey) {
  throw new Error('OpenRouter API Key not configured in environment variables.');
}

export const createOpenRouterClient = (model: string, temperature: number = 0.7): ChatOpenAI => {
  return new ChatOpenAI({
    modelName: model,
    temperature: temperature,
    openAIApiKey: config.openRouterApiKey,
    configuration: {
      baseURL: 'https://openrouter.ai/api/v1',
    },
  });
};
