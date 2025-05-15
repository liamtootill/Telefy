<p align="center">
  <img src="https://github.com/telefydotfun/Telefy/blob/main/web/public/images/banner-twitter/banner%20twitter.png"/>
</p>

**TELEFY** is a next-generation AI-powered bot for Telegram and Twitter (X), designed to provide intelligent, context-aware conversations with persistent memory. It leverages advanced LLMs (via OpenRouter and LangChain), supports group and private chats, and is built for extensibility and future integration with a Solana-based utility token.

---

## Features

### Telegram Bot
- **Group & Private Chat Support:** Responds in both private and group chats, with mention/reply triggers in groups.
- **Persistent Memory:** Remembers conversation context per chat, summarizing and saving to Supabase every 10 messages for efficiency.
- **Custom Prompts:** Admins can set custom system prompts for their group or chat.
- **Admin Controls:** Only group admins can change key settings (e.g., custom prompts).
- **Rate Limiting:** Prevents spam with configurable rate limits and user feedback.
- **Modern AI Personality:** Uncensored, direct, and customizable via prompt.

### Twitter (X) Bot
- **Mentions & Tweet Handling:** Listens for mentions and tweets, responds intelligently.
- **Memory:** Maintains a memory buffer for ongoing context.
- **Custom System Prompt:** Configurable system prompt for consistent persona.

### AI Integration
- **OpenRouter & LangChain:** Uses OpenRouter for LLM access and LangChain for memory and agent logic.
- **Summary Buffer Memory:** Efficiently summarizes and stores conversation history.

### Memory Management
- **Supabase Integration:** All memory and configuration is stored in Supabase for reliability and scalability.
- **Per-Chat/Group Memory:** Each chat/group has its own memory and settings.
- **Periodic Summary Saving:** Summaries are only saved to the database every 10 messages per chat/group for performance.

### ⚙Configuration & Extensibility
- **Environment Variables:** All sensitive data and API keys are managed via environment variables.
- **Modular Structure:** Clean, scalable codebase for easy maintenance and extension.

### Solana Token Integration (Coming Soon)
- **$TELEFY Utility Token:** The bot will soon integrate with a Solana-based token for unlocking premium features, custom actions, and more.
- **Contract Address:** _Coming soon_

---

## Getting Started

### Prerequisites
- Node.js (v18+ recommended)
- Supabase account & project
- OpenRouter API key
- Telegram Bot Token
- Twitter (X) Developer credentials

### Installation

```bash
# Clone the repository
$ git clone https://github.com/Belucard/Telefy.git

# Install dependencies
$ npm install
```

### Configuration
1. Copy `.env.example` to `.env` and fill in all required variables:

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENROUTER_API_KEY=your-openrouter-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
TWITTER_BEARER_TOKEN=your-twitter-bearer-token
```

2. Set up your Supabase database with the required tables (`telegram_memories`, `twitter_memory`).

### Running the Bot

```bash
# Start the Telegram and Twitter bots
$ npm run start
```

---

## Environment Variables

| Variable              | Description                        |
|-----------------------|------------------------------------|
| TELEGRAM_BOT_TOKEN    | Telegram bot API token             |
| OPENROUTER_API_KEY    | OpenRouter API key                 |
| SUPABASE_URL          | Supabase project URL               |
| SUPABASE_KEY          | Supabase API key                   |
| TWITTER_BEARER_TOKEN  | Twitter API bearer token           |

---

## Links

- **X/Twitter:** [Follow us on X/Twitter](https://x.com/telefydotfun)  
- **Solana Contract:** _Coming soon_

---

## Contributing

Pull requests and issues are always welcome! Join us and help shape Telefy!

## License

## Contact

For questions, suggestions, or support, open an issue or reach out via [X/Twitter](https://twitter.com/yourproject). 
