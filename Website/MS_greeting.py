# MS_greeting.py
from flask import Flask, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__)

def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good morning"
    elif 12 <= current_hour < 18:
        return "Good afternoon"
    else:
        return "Good night"

@app.route('/greetAPI', methods=['GET'])
def greet():
    greeting = get_greeting()
    return jsonify({"Greeting": greeting})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
