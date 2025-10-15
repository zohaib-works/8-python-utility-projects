from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('website/index.html')



@app.route('/get-weather', methods=['POST'])
def get_weather():
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude'})

    api_key = '276e8b7b82a0240a58326ba6f8215589'
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'

    try:
        res = requests.get(url).json()
        weather = {
            "location": f"{res['name']}, {res['sys']['country']}",
            "temperature": res['main']['temp'],
            "description": res['weather'][0]['description'].capitalize(),
            "icon": f"http://openweathermap.org/img/wn/{res['weather'][0]['icon']}@2x.png"


        }
        return jsonify(weather)
    except Exception as e:
        return jsonify({'error': "Failed to retrieve weather data."}), 500
    



    response = requests.get(url)
    data = json.loads(response.text)    
    if data['cod'] == 200:
        weather = data['weather'][0]['main']    
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        return render_template('index.html', weather=weather, temperature=temperature, humidity=humidity, wind_speed=wind_speed)
    else:
        flash('City not found!')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True) 