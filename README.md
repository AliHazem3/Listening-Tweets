# Listening-Tweets

How  to Run 
Project
Start the Server:
Open a terminal/command prompt
Run:  python Tweets_Listen.py

you should see
     WebSocket server started on ws://localhost:8765
     Monitoring tweets from @elonmusk...

Start the Client:
Open another terminal/command prompt
Navigate to the same project directory
Run: python client.py


1. Server Side (Tweets_Listen.py):
Starts a WebSocket server on port 8765
Connects to Twitter API
Gets @elonmusk's latest tweets
Sends tweets to any connected clients
Checks for new tweets every 30 seconds

2. Client Side (client.py):
Connects to the WebSocket server
Receives tweets in real-time
Displays each tweet with:
Text content
Username (@elonmusk)
Timestamp
Automatically reconnects if connection is lost
