# MA_udn.py
import requests

def send_notification():
    url = 'http://localhost:5003/unot'
    data = {
        'username': 'Joon',
        'action(upload/delete)': "upload",
        'mtext': 'testing text'
    }
    response = requests.post(url, json=data)
    print(response.json())

if __name__ == '__main__':
    send_notification()