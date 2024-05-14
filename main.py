from flask import Flask, render_template, request
import requests, base64
from datetime import datetime

api_key = "28662158-d89a-4a27-a202-0584ee64e9cf:ecf887cc93015e93ba12e7deec48f22837cdab04b352f4a60ce7e7c748c84e92b8ad0120944c8c1a16b28c50b9effbd626e57cdfdf6b74dac368814da98ebdfdac392c47290de1ddfc96ed3fe94e68ef2961c30ba3e292107ca1da2c4e99e4328396a0c2fbb98c2bb5f402c96ef08eb9"

app = Flask(__name__)

DEVELOPMENT_ENV = True

@app.route('/', methods=['GET'])
def index():
    print(request.headers.get('X-Forwarded-For', request.remote_addr))
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr) #request.remote_addr

    data = requests.get(f"http://ip-api.com/json/{user_ip}").json()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(api_key.encode()).decode()}',
    }
    json_data = {
        "format": "png",
        "style": {
            "moonStyle": "sketch",
            "backgroundStyle": "stars",
            "backgroundColor": "red",
            "headingColor": "white",
            "textColor": "red"
        },
        "observer": {
            "latitude": data['lat'],
            "longitude": data['lon'],
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        "view": {
            "type": "portrait-simple",
            #"orientation": "south-up"
        }
    }
    response_moon_image = requests.post('https://api.astronomyapi.com/api/v2/studio/moon-phase', headers=headers, json=json_data).json()['data']['imageUrl']

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {base64.b64encode(api_key.encode()).decode()}',
    }
    json_data = {
        "style": "inverted",
        "observer": {
            "latitude": data['lat'],
            "longitude": data['lon'],
            "date": datetime.now().strftime("%Y-%m-%d")
        },
        "view": {
            "type": "constellation",
            "parameters": {
                "constellation": "and"
            }
        }
    }
    response_stars_image = requests.post('https://api.astronomyapi.com/api/v2/studio/star-chart', headers=headers, json=json_data).json()['data']['imageUrl']


    

    
    return render_template("index.html", image=response_moon_image, image2=response_stars_image, ip=user_ip) 


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, port=5000, threaded=True)