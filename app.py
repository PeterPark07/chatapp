from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from datetime import datetime, timedelta

import eventlet
eventlet.monkey_patch()
from database import messages_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = list(messages_collection.find({}, {'_id': 0, 'username': 1, 'message': 1, 'time': 1, 'date': 1}))

users_online = 0

def get_current_time():
    utc_now = datetime.utcnow()
    time_plus_5_30 = utc_now + timedelta(hours=5, minutes=30)
    return time_plus_5_30.strftime('%I:%M %p')

def get_current_date():
    current_date = datetime.utcnow() + timedelta(hours=5, minutes=30)
    return current_date.strftime('%d %B, %Y')

@app.route('/')
def chat():
    messages = list(messages_collection.find({}, {'_id': 0, 'username': 1, 'message': 1, 'time': 1, 'date': 1}))
    
    last_date = ''
    
    for message in messages:
        if message['date'] != last_date:
            message['new_date'] = message['date']
            last_date = message['date']
    
    
    return render_template('chat.html', messages=messages, current_date= get_current_date())

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
    
    new_message = {'username': username, 'message': data['message'], 'time': get_current_time(), 'date': get_current_date()}
    send(new_message, broadcast=True)
    messages_collection.insert_one(new_message)

if __name__ == '__main__':
    socketio.run(app, debug=True)