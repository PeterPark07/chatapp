from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

messages = [
    {'username': 'Alice', 'message': 'Hello, everyone! I hope you are all having a great day!', 'time': '10:00 AM'},
    {'username': 'Bob', 'message': 'Hi Alice! How are you? I was just thinking about the project we discussed last week.', 'time': '10:01 AM'},
    {'username': 'Charlie', 'message': 'Hey folks, what’s up? I have some exciting news to share with you all.', 'time': '10:02 AM'},
    {'username': 'Alice', 'message': 'That sounds great, Charlie! What’s the news? I’m curious to know more about it.', 'time': '10:03 AM'},
    {'username': 'Bob', 'message': 'Yes, Charlie, do tell us more! We could all use some good news right now.', 'time': '10:04 AM'},
    {'username': 'Charlie', 'message': 'Well, I just got promoted at work! It’s been a long journey, but it finally paid off.', 'time': '10:05 AM'}
]

users_online = 0

def get_current_time_plus_5_30():
    utc_now = datetime.utcnow()
    time_plus_5_30 = utc_now + timedelta(hours=5, minutes=30)
    return time_plus_5_30.strftime('%I:%M %p')

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
    current_time = get_current_time_plus_5_30()
    new_message = {'username': 'User', 'message': data, 'time': current_time}
    messages.append(new_message)
    app.logger.info(f'New message: {new_message}')
    send(new_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)