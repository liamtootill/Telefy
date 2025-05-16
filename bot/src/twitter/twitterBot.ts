import { TwitterApi } from 'twitter-api-v2';
import { config } from '../config';
import { handleMention } from './handlers/mentionHandler';
import { handleTweet } from './handlers/tweetHandler';

if (!config.twitterBearerToken) {
  console.warn('Twitter Bearer Token not configured. Twitter bot features disabled.');
}

// Use App context
const twitterClient = config.twitterBearerToken ? new TwitterApi(config.twitterBearerToken) : null;

// Readonly client
const roClient = twitterClient?.readOnly;

export const startTwitterBot = async () => {
  if (!roClient || !twitterClient) {
    console.log('Twitter client not initialized. Skipping Twitter bot startup.');
    return;
  }

  console.log('Starting Twitter bot stream...');

  // Auto-tweet every 30 minutes
  setInterval(() => {
    handleTweet(twitterClient);
  }, 30 * 60 * 1000); // 30 minutes

  try {
    const stream = await roClient.v2.searchStream({
        'tweet.fields': ['referenced_tweets', 'author_id'],
        expansions: ['referenced_tweets.id', 'author_id'],
      });
    stream.autoReconnect = true;

    stream.on('data event', async (eventData) => {
      console.log("Twitter received event data:", eventData)
      // Check if it's a mention and not a retweet or reply to own tweet
      const isMention = eventData.data.referenced_tweets?.some((ref: { type: string; id: string }) => ref.type === 'replied_to') && 
                        eventData.data.author_id !== (await roClient.v2.me()).data.id;
      
      if (isMention) {
        await handleMention(eventData, twitterClient);
      }
    });

    stream.on('connected event', () => {
      console.log('Twitter stream connected!');
    });

    stream.on('error event', (error) => {
        console.error("Twitter stream error:", error)
    })

    stream.on('connection error event', (error) => {
        console.error("Twitter connection error:", error)
    })

    stream.on('reconnect error event', (error) => {
        console.error("Twitter reconnect error:", error)
    })

    // Handle graceful shutdown
    process.once('SIGINT', () => stream.close());
    process.once('SIGTERM', () => stream.close());

  } catch (error) {
    console.error('Failed to start Twitter stream:', error);
  }
};
