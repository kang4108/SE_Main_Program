#MS_pn.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def notify():
    data = request.get_json()
    user = data.get('user')
    action = data.get('action')
    message = f"Notification: User {user} has {action} a post"
    print(message)
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(port=5002)







