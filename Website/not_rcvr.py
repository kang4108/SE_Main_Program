# not_rcvr.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/unot', methods=['POST'])
def notification():
        data = request.get_json()
        username = data.get('username')
        action = data.get('action(upload/delete)')
        text = data.get('mtext')
        print(f'Notification: {username} wants to {action} the text [{text}].')
        return jsonify({"message": "Notification received"}), 200

if __name__ == '__main__':
    app.run(port=5003)