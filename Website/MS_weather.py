from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'cf7616dd57a4c7036dd6c9b500b0da7b'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city') 
    if not city:
        return jsonify({"error": "City is required"}), 400
    
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather = {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'city': data['name'],
            'country': data['sys']['country']
        }
        return jsonify(weather), 200
    else:
        return jsonify({"error": "City not found"}), 404

if __name__ == '__main__':
    app.run(port=5002, host='0.0.0.0', debug=True)
