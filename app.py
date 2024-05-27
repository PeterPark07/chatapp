from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def chat():
    # Sample messages
    messages = [
        {'username': 'Alice', 'message': 'Hello, everyone!'},
        {'username': 'Bob', 'message': 'Hi Alice! How are you?'},
        {'username': 'Charlie', 'message': 'Hey folks, what’s up?'}
    ]
    return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
