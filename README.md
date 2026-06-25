# Chat Application

A real-time, multi-user web chat application with music streaming, theme customization, and persistent message storage.

## Features

✨ **Real-Time Messaging** – Instant message delivery using WebSocket (Flask-SocketIO)

🎨 **Theme System** – Three color themes (light, pink, blue) plus dark mode toggle

🎵 **Music Integration** – Search and stream YouTube audio directly in chat using `/play [query]`

👥 **Live User Count** – Track active users with page visibility detection

💾 **Message Persistence** – All messages stored in MongoDB for chat history

📱 **Responsive Design** – Clean, modern UI with Roboto font

🎯 **Message Threading** – Consecutive messages from the same user in the same minute display compactly

## Tech Stack

- **Backend:** Flask + Flask-SocketIO + eventlet
- **Database:** MongoDB
- **Frontend:** HTML5, CSS3, JavaScript (Socket.IO client)
- **Music:** yt-dlp + youtube-search-python

## Installation

### Prerequisites

- Python 3.7 or higher
- MongoDB instance running locally or remotely
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PeterPark07/chatapp.git
   cd chatapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   export mongodb="mongodb://localhost:27017"
   export collection="messages"
   ```
   Replace with your MongoDB connection string and desired collection name.

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the chat:**
   Open your browser to `http://localhost:5000` and enter a username to start chatting.

## Usage

### Basic Chat

- Type a message and press **Send** to broadcast to all connected users
- Your username is stored as a cookie for 7 days
- Messages display with username, timestamp, and date separators

### Commands

#### Theme Commands

```bash
/theme 1          # Light theme
/theme 2          # Pink theme
/theme 3          # Blue theme
/theme dark       # Enable dark mode
/theme light      # Disable dark mode
```

#### Music Commands

```bash
/play [song]      # Search YouTube and stream audio (e.g., /play Never Gonna Give You Up)
/play             # Resume music
/pause            # Pause music
/loop             # Toggle loop on current track
```

## Project Structure

```
app.py              # Main Flask app, Socket.IO event handlers
database.py         # MongoDB connection setup
helper.py           # Time and date utilities (UTC+5:30)
music.py            # YouTube search and audio download logic
requirements.txt    # Python dependencies
templates/
  └─ chat.html      # Chat UI with embedded CSS and theme styles
static/
  └─ script.js      # Socket.IO client, event listeners, UI updates
```

## How It Works

1. **Connection Phase**
   - User opens the app and enters a username (stored in a 7-day cookie)
   - Client connects to Socket.IO server and requests all previous messages from MongoDB

2. **Message Flow**
   - User sends a message via form submission
   - Backend determines if message is "followed" (from same user, same minute)
   - Message is broadcast to all connected clients and inserted into MongoDB
   - Clients render the message with appropriate styling

3. **Real-Time Features**
   - Page visibility changes emit `page_visible` or `page_hidden` events
   - Online user count is computed server-side and broadcast to all clients
   - Theme and dark mode changes are broadcast globally to all connected users
   - Music playback commands trigger downloads and audio streaming to all clients

## API / Socket.IO Events

### Client → Server

| Event | Data | Description |
|-------|------|-------------|
| `message` | `{username, message}` | Send a chat message |
| `connect` | — | User connects |
| `disconnect` | — | User disconnects |
| `page_visible` | — | Tab/window becomes visible |
| `page_hidden` | — | Tab/window is hidden |

### Server → Clients

| Event | Data | Description |
|-------|------|-------------|
| `message` | `{username, message, time, date, followed}` | Broadcast message to all |
| `followed_message` | `{username, message, time, date, followed}` | Message from same user, same minute |
| `change_theme` | `'1' \| '2' \| '3'` | Apply theme globally |
| `dark_mode` | — | Enable dark mode globally |
| `dark_mode_off` | — | Disable dark mode globally |
| `play_music` | `{url}` | Play audio at URL |
| `pause_music` | — | Pause playback |
| `unpause_music` | — | Resume playback |
| `loop_music` | — | Toggle loop state |
| `users_online` | `count` | Update online user count |

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `mongodb` | MongoDB connection string | `mongodb://localhost:27017` |
| `collection` | MongoDB collection name for messages | `messages` |

## License

This project is licensed under the **GNU General Public License v3.0** – see the [LICENSE](LICENSE) file for details.

## Future Enhancements

- User authentication and profiles
- Private messaging and rooms
- Message reactions and emoji support
- File sharing
- Message search and filtering
- Admin controls for moderation
- Mobile app with React Native

## Contributing

Contributions are welcome! Feel free to fork the repo, create a feature branch, and submit a pull request.

## Author

[PeterPark07](https://github.com/PeterPark07)

---

**Questions?** Open an issue or reach out on GitHub!
