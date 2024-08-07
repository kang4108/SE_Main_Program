# SE_Main_Program
# Joonbum Kang
# test commit

#communication contract
1. To request data from Microservice A, you need "MA_pn.py" which is provided below.
   Run the file with the microservice on seperate terminals and it'll request the data of username and action about their post.
2. To receive data from Microservice A, keep the file running on the terminal.
   If either a post is uploaded or deleted in the microservice, you'll receive the requested data from it.

#MA_pn.py
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
