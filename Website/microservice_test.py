import requests

def test_notify():
    url = 'http://localhost:5002/notify'
    data = {
        'user': 'Joon',
        'action': 'uploaded a post'
    }
    response = requests.post(url, json=data)
    print(response.json())

if __name__ == '__main__':
    test_notify()