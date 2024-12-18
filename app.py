from flask import Flask, request, jsonify, render_template
import requests
import base64

app = Flask(__name__)

OPENWEATHER_API_KEY = 'b571467ac02141716798e4555baa27 68'

SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
    response = requests.get(url)
    return response.json()


def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode((SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode('utf-8')).decode('utf-8')
    }
    response = requests.post(auth_url, data=auth_data, headers=auth_headers)
    return response.json().get('access_token')


def get_playlist(weather, mood):
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }

    url = 'https://api.spotify.com/v1/browse/featured-playlists'
    response = requests.get(url, headers=headers)
    playlists = response.json().get('playlists', {}).get('items', [])
    return [playlist['name'] for playlist in playlists]


@app.route('/generate_playlist', methods=['POST'])
def generate_playlist():
    data = request.json
    city = data.get('city')
    mood = data.get('mood')

    weather = get_weather(city)
    playlist = get_playlist(weather, mood)

    return jsonify({'playlist': playlist})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

