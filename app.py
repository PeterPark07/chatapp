from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

messages = [
    {'username': 'Alice', 'message': 'Hello, everyone! I hope you are all having a great day!', 'time': '10:00 AM'},
    {'username': 'Bob', 'message': 'Hi Alice! How are you? I was just thinking about the project we discussed last week.', 'time': '10:01 AM'},
    {'username': 'Charlie', 'message': 'Hey folks, what’s up? I have some exciting news to share with you all.', 'time': '10:02 AM'},
    {'username': 'Alice', 'message': 'That sounds great, Charlie! What’s the news? I’m curious to know more about it.', 'time': '10:03 AM'},
    {'username': 'Bob', 'message': 'Yes, Charlie, do tell us more! We could all use some good news right now.', 'time': '10:04 AM'},
    {'username': 'Charlie', 'message': 'Well, I just got promoted at work! It’s been a long journey, but it finally paid off.', 'time': '10:05 AM'}
]

@app.route('/')
def chat():
    return render_template('chat.html', messages=messages, current_date=datetime.now().strftime('%B %d, %Y'))

@socketio.on('message')
def handle_message(data):
    current_time = datetime.now().strftime('%I:%M %p')
    new_message = {'username': 'User', 'message': data, 'time': current_time}
    messages.append(new_message)
    send(new_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)