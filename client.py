import asyncio
import websockets
import json
import sys

async def listen_to_messages():
    uri = "ws://localhost:8765"
    while True:
        try:
            print("🔄 Connecting to WebSocket server...")
            async with websockets.connect(uri) as websocket:
                print("✅ Connected to WebSocket server!")
                print("📡 Waiting for messages...")
                
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        print(f"\n📝 New message from {data['username']}:")
                        print(f"   Text: {data['text']}")
                        print(f"   Time: {data['created_at']}")
                    except websockets.exceptions.ConnectionClosed:
                        print("❌ Connection closed by server. Reconnecting...")
                        break
        except ConnectionRefusedError:
            print("❌ Could not connect to server. Make sure Tweets_Listen.py is running.")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)

async def main():
    try:
        await listen_to_messages()
    except KeyboardInterrupt:
        print("\n👋 Client stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())