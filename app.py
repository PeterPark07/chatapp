from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from helper import get_current_time, get_current_date

import eventlet
eventlet.monkey_patch()
from database import messages_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = list(messages_collection.find({}, {'_id': 0, 'username': 1, 'message': 1, 'time': 1, 'date': 1}))

users_online = 0

@app.route('/')
def chat():
    messages = list(messages_collection.find({}, {'_id': 0, 'username': 1, 'message': 1, 'time': 1, 'date': 1}))
    
    last_date = ''
    
    for message in messages:
        if message['date'] != last_date:
            message['new_date'] = message['date']
            last_date = message['date']
    
    return render_template('chat.html', messages=messages)

@socketio.on('connect')
def handle_connect():
    global users_online
    users_online += 1
    emit('users_online', users_online, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global users_online
    users_online -= 1
    emit('users_online', users_online, broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'User')
    message = data['message']
    
    if message.startswith('/theme'):
        theme_command = message.split(' ')[1]
        if theme_command in ['1', '2', 'dark', 'blue']:
            emit('change_theme', theme_command, broadcast=True)
    
    new_message = {'username': username, 'message': message, 'time': get_current_time(), 'date': get_current_date()}
    send(new_message, broadcast=True)
    messages_collection.insert_one(new_message)

if __name__ == '__main__':
    socketio.run(app, debug=True)
