from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    user = data.get('user')
    action = data.get('action')
    message = f"Notification: {user} performed {action}."
    print(message)
    # Simulate sending a notification
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(port=5002)