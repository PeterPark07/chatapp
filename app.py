from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from datetime import datetime, timedelta
from database import messages_collection

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = []

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
    return render_template('chat.html', messages=messages, current_date=datetime.now().strftime('%B %d, %Y'))

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
    new_message = {'username': 'User', 'message': data, 'time': get_current_time(), 'date': get_current_date()}
    messages_collection.insert_one(new_message)
    messages.append(new_message)
    send(new_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)