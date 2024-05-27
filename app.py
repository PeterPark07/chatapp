from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chat():
    # Sample messages with timestamps and longer text
    messages = [
        {'username': 'Alice', 'message': 'Hello, everyone! I hope you are all having a great day!', 'time': '10:00 AM'},
        {'username': 'Bob', 'message': 'Hi Alice! How are you? I was just thinking about the project we discussed last week.', 'time': '10:01 AM'},
        {'username': 'Charlie', 'message': 'Hey folks, what’s up? I have some exciting news to share with you all.', 'time': '10:02 AM'},
        {'username': 'Alice', 'message': 'That sounds great, Charlie! What’s the news? I’m curious to know more about it.', 'time': '10:03 AM'},
        {'username': 'Bob', 'message': 'Yes, Charlie, do tell us more! We could all use some good news right now.', 'time': '10:04 AM'},
        {'username': 'Charlie', 'message': 'Well, I just got promoted at work! It’s been a long journey, but it finally paid off.', 'time': '10:05 AM'}
    ]

    if request.method == 'POST':
        username = 'User'  # In a real application, this would be dynamic
        message_text = request.form['message']
        current_time = datetime.now().strftime('%I:%M %p')
        
        new_message = {'username': username, 'message': message_text, 'time': current_time}
        messages.append(new_message)

    return render_template('chat.html', messages=messages, current_date=datetime.now().strftime('%B %d, %Y'))

if __name__ == '__main__':
    app.run(debug=True)
