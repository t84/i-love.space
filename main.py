from flask import Flask, render_template, request, jsonify
import requests, base64
from datetime import datetime, timedelta
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


api_key = "28662158-d89a-4a27-a202-0584ee64e9cf:ecf887cc93015e93ba12e7deec48f22837cdab04b352f4a60ce7e7c748c84e92b8ad0120944c8c1a16b28c50b9effbd626e57cdfdf6b74dac368814da98ebdfdac392c47290de1ddfc96ed3fe94e68ef2961c30ba3e292107ca1da2c4e99e4328396a0c2fbb98c2bb5f402c96ef08eb9"
apikey = "49be3a765aa44ec1a02e6baddcaaeb50"
app = Flask(__name__)

DEVELOPMENT_ENV = True


# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})




@app.route('/', methods=['GET'])
def index():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        data = requests.get(f"http://ip-api.com/json/{user_ip}", timeout=5).json()
        
        r = requests.get('https://api.wheretheiss.at/v1/satellites/25544').json()

        headers = {
            'User-Agent': 'https://i-love.space',
            'Referer': 'https://i-love.space',  
        }


        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={r['latitude']}&lon={r['longitude']}&apiKey={apikey}"

        r2 = requests.get(url, headers=headers).json()        
        country_name = r2['features'][0]['properties']['name']
        
        iss_json = {"data": {"coordinates": {"latitude": r['latitude'], "longitude": r['longitude']}, "country_name": country_name}}


        return render_template("index.html", country=iss_json['data']['country_name'], lat=iss_json['data']["coordinates"]['latitude'], lon=iss_json['data']["coordinates"]['longitude'], ip=user_ip)
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return "An error occurred while fetching data. Please try again later."
    

@app.route('/api/update_iss', methods=['GET'])
def update_iss():
    cached_response = cache.get('update_iss_response')
    if cached_response:
        return jsonify(cached_response, "THIS WAS CACHED")

    r = requests.get('https://api.wheretheiss.at/v1/satellites/25544').json()
    headers = {
        'User-Agent': 'https://i-love.space',
        'Referer': 'https://i-love.space',  
    }
    url = f"https://api.geoapify.com/v1/geocode/reverse?lat={r['latitude']}&lon={r['longitude']}&apiKey={apikey}"
    r2 = requests.get(url, headers=headers).json()        
    country_name = r2['features'][0]['properties']['name']

    response_data = {"data": {"coordinates": {"latitude": r['latitude'], "longitude": r['longitude']}, "country_name": country_name}}

    cache.set('update_iss_response', response_data, timeout=10)

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, port=5000, threaded=True)