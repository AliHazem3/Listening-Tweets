import tweepy
import websockets
import asyncio
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

# Initialize Twitter client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Target account to monitor
TARGET_USERNAME = "elonmusk"

async def get_user_id(username):
    """Get user ID from username"""
    try:
        user = client.get_user(username=username)
        if user.data:
            return user.data.id
        return None
    except Exception as e:
        print(f"Error getting user ID: {e}")
        return None

async def get_latest_tweets(user_id, count=5):
    """Get latest tweets from user"""
    try:
        tweets = client.get_users_tweets(
            user_id,
            max_results=count,
            tweet_fields=['created_at', 'text']
        )
        return tweets.data if tweets.data else []
    except Exception as e:
        print(f"Error getting tweets: {e}")
        return []

async def stream_messages(websocket):
    """Stream real tweets to the client"""
    try:
        user_id = await get_user_id(TARGET_USERNAME)
        if not user_id:
            await websocket.send(json.dumps({"error": "User not found"}))
            return

        # Get initial tweets
        tweets = await get_latest_tweets(user_id)
        for tweet in tweets:
            message = {
                "text": tweet.text,
                "username": TARGET_USERNAME,
                "created_at": tweet.created_at.isoformat()
            }
            await websocket.send(json.dumps(message))

        # Keep checking for new tweets
        last_tweet_id = tweets[0].id if tweets else None
        while True:
            await asyncio.sleep(30)  # Check every 30 seconds
            
            new_tweets = await get_latest_tweets(user_id)
            if new_tweets and new_tweets[0].id != last_tweet_id:
                for tweet in new_tweets:
                    if tweet.id == last_tweet_id:
                        break
                    message = {
                        "text": tweet.text,
                        "username": TARGET_USERNAME,
                        "created_at": tweet.created_at.isoformat()
                    }
                    await websocket.send(json.dumps(message))
                last_tweet_id = new_tweets[0].id

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")

async def handler(websocket, path):
    """WebSocket handler"""
    print("New client connected")
    await stream_messages(websocket)

async def main():
    """Start WebSocket server"""
    try:
        server = await websockets.serve(handler, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765")
        print(f"Monitoring tweets from @{TARGET_USERNAME}...")
        await server.wait_closed()
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
