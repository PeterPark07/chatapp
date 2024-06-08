from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from helper import get_current_time, get_current_date
from music import download_music, delete_music_folder

import eventlet
eventlet.monkey_patch()
from database import messages_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Directory to save downloaded music files
MUSIC_DIR = 'static/music'

# Track connected users and their visibility state
users_online = 0

# Store last message details in memory for quick access
last_message_details = {
    'username': None,
    'time': None
}

def fetch_messages():
    messages = list(messages_collection.find({}, {'_id': 0, 'username': 1, 'message': 1, 'time': 1, 'date': 1, 'followed': 1}))
    last_date = ''
    for message in messages:
        if message['date'] != last_date:
            message['new_date'] = message['date']
            last_date = message['date']
    return messages

@app.route('/')
def chat():
    messages = fetch_messages()
    return render_template('chat.html', messages=messages)


@socketio.on('connect')
def handle_page_visible():
    global users_online
    users_online += 1
    socketio.emit('users_online', users_online, broadcast=True)

@socketio.on('disconnect')
def handle_page_hidden():
    global users_online
    users_online -= 1
    socketio.emit('users_online', users_online, broadcast=True)



@socketio.on('page_visible')
def handle_page_visible():
    global users_online
    users_online += 1
    socketio.emit('users_online', users_online, broadcast=True)

@socketio.on('page_hidden')
def handle_page_hidden():
    global users_online
    users_online -= 1
    socketio.emit('users_online', users_online, broadcast=True)

@socketio.on('message')
def handle_message(data):
    global last_message_details

    username = data.get('username', 'User')
    message = data['message']
    current_time = get_current_time()
    current_date = get_current_date()

    if message.startswith('/theme'):
        theme_commands = message.split()

        # Handle theme number (1, 2, 3)
        if '1' in theme_commands:
            emit('change_theme', '1', broadcast=True)
        elif '2' in theme_commands:
            emit('change_theme', '2', broadcast=True)
        elif '3' in theme_commands:
            emit('change_theme', '3', broadcast=True)

        # Handle dark/light mode
        if 'dark' in theme_commands:
            emit('dark_mode', broadcast=True)
        elif 'light' in theme_commands:
            emit('dark_mode_off', broadcast=True)

    # Check if the last message is from the same user and within a minute
    followed = 0
    if last_message_details['username'] == username and last_message_details['time'] == current_time:
        followed = 1

    new_message = {
        'username': username,
        'message': message,
        'time': current_time,
        'date': current_date,
        'followed': followed
    }

    # Broadcast message as followed or not followed
    if followed:
        emit('followed_message', new_message, broadcast=True)
    else:
        send(new_message, broadcast=True)


    # Update last message details
    last_message_details = {
        'username': username,
        'time': current_time
    }

    if message.startswith('/play '):
        query = message[6:]
        delete_music_folder(MUSIC_DIR)
        filename = download_music(query, MUSIC_DIR)
        if filename:
            url = f'/{filename}'
            emit('play_music', {'url': url}, broadcast=True)
        else:
            emit('music_download_failed', {'message': 'Unable to download music.'})

    if message == '/pause':
        emit('pause_music', broadcast=True)

    if message == '/play':
        emit('unpause_music', broadcast=True)
    if message == '/loop':
        emit('loop_music', broadcast=True)

    # Insert message into the database
    messages_collection.insert_one(new_message)

if __name__ == '__main__':
    socketio.run(app, debug=True)