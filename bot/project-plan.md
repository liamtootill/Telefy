# 🚀 AI Agent Project Plan (Detailed & Scalable)

## 📌 Project Overview

We will build a scalable AI agent that:

- Runs as a Telegram bot, supporting multiple group chats simultaneously.
- Maintains isolated memory, personality, and AI model preferences per group chat.
- Integrates with OpenRouter to access multiple AI models dynamically.
- Uses Supabase for persistent memory storage, ensuring scalability and reliability.
- Manages a Twitter account with a separate personality and memory, using a custom system prompt for unfiltered AI responses.

---

## 🛠️ Tech Stack

| Component              | Technology / Framework |
|------------------------|------------------------|
| Telegram Bot           | Telegraf.js            |
| AI Integration         | LangChain.js           |
| AI Provider            | OpenRouter             |
| Persistent Storage     | Supabase               |
| Twitter Integration    | Twitter.js             |
| Language               | TypeScript             |
| Environment            | Node.js                |

---

## 📂 Project Structure (Detailed)

## ✅ Implementation Steps
project-root/
├── src/
│ ├── telegram/
│ │ ├── bot.ts # Telegram bot initialization & middleware
│ │ ├── handlers/
│ │ │ ├── messageHandler.ts # Message handling logic
│ │ │ └── commandHandler.ts # Command handling logic
│ │ └── middleware/
│ │ └── memoryMiddleware.ts # Middleware for memory & personality
│ │
│ ├── twitter/
│ │ ├── twitterBot.ts # Twitter bot initialization & logic
│ │ ├── handlers/
│ │ │ ├── mentionHandler.ts # Handling mentions & replies
│ │ │ └── tweetHandler.ts # Posting tweets logic
│ │ └── prompts/
│ │ └── systemPrompt.ts # Custom system prompt for Twitter agent
│ │
│ ├── ai/
│ │ ├── openrouterClient.ts # OpenRouter API client setup
│ │ └── langchain.ts # LangChain.js setup & utilities
│ │
│ ├── memory/
│ │ └── supabaseMemory.ts # Supabase memory storage integration
│ │
│ ├── config/
│ │ └── index.ts # Environment variables & config management
│ │
│ └── utils/
│ └── helpers.ts # Common helper functions
│
├── .env # Environment variables
├── package.json
├── tsconfig.json
└── README.md


---

## ✅ Implementation Steps (Detailed & AI-Friendly)

### 1. Project Initialization

Initialize Node.js project with TypeScript:

```bash
npm init -y
npm install typescript ts-node @types/node dotenv
npx tsc --init
```

Install dependencies:

```bash
npm install telegraf langchain @supabase/supabase-js twitter-api-v2 openai
```

---

### 2. Supabase Setup (Detailed)

Create a Supabase project at [supabase.com](https://supabase.com).

Define tables clearly:

**Table:** `telegram_memories`

| Column       | Type    | Description                      |
|--------------|---------|----------------------------------|
| chat_id      | bigint  | Telegram chat ID (primary key)   |
| memory       | text    | Conversation memory/history      |
| personality  | text    | Personality prompt               |
| model        | text    | Preferred AI model               |

**Table:** `twitter_memory`

| Column       | Type    | Description                      |
|--------------|---------|----------------------------------|
| id           | text    | Identifier (e.g., "twitter_bot") |
| memory       | text    | Conversation memory/history      |
| personality  | text    | Personality prompt               |
| model        | text    | Preferred AI model               |

---

### 3. AI Integration (OpenRouter & LangChain.js)

Set up OpenRouter client and LangChain.js utilities:

- `src/ai/openrouterClient.ts`
- `src/ai/langchain.ts`

---

### 4. Memory Management (Supabase Integration)

Implement memory storage and retrieval logic:

- `src/memory/supabaseMemory.ts`

---

### 5. Telegram Bot Implementation (Scalable Middleware)

Implement Telegram bot initialization, middleware, and handlers:

- `src/telegram/bot.ts`
- `src/telegram/middleware/memoryMiddleware.ts`
- `src/telegram/handlers/messageHandler.ts`

---

### 6. Twitter Bot Implementation (Custom System Prompt)

Implement Twitter bot initialization, handlers, and custom system prompt:

- `src/twitter/twitterBot.ts`
- `src/twitter/handlers/mentionHandler.ts`
- `src/twitter/prompts/systemPrompt.ts`

---

### 7. Environment Variables (`.env`)

Clearly defined environment variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
OPENROUTER_API_KEY=your_openrouter_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
TWITTER_BEARER_TOKEN=your_twitter_token
```

---

### 8. Testing & Deployment

- Test each component individually.
- Deploy using Docker or a cloud provider (e.g., Railway, Render, AWS, Vercel).

---

### 9. Scalability & Performance Considerations

- Supabase ensures scalability for thousands of concurrent users.
- Middleware architecture isolates memory per chat, ensuring no cross-chat interference.
- LangChain.js efficiently manages memory and context.

---

## 🚧 Future Enhancements (Clearly Defined)

- Admin dashboard for managing personalities, models, and memory.
- Advanced memory management (vector embeddings, semantic search).
- Scheduled tweets and proactive interactions.
- Analytics and monitoring dashboard.

---

## 📖 Documentation & Maintenance

- Maintain clear documentation in `README.md`.
- Regularly update dependencies and perform security audits.
- Monitor logs and performance metrics for continuous improvement.

---

## 🎯 Conclusion

This detailed, structured, and scalable project plan provides clear, step-by-step instructions suitable for AI-assisted or junior developer implementation, ensuring robust scalability and maintainability.