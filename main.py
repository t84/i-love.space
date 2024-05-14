from flask import Flask, render_template, request
from assets.functions import *
import requests


app = Flask(__name__)

DEVELOPMENT_ENV = True

@app.route('/', methods=['GET'])
def index():
    print(request.headers.get('X-Forwarded-For', request.remote_addr))
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr) #request.remote_addr
    if user_ip != "127.0.0.1":

        location_data = get_location(user_ip)
        moon_image_url = get_moon_phase(location_data)
        star_chart_image_url = get_star_chart("ori", location_data)
    
        return render_template("index.html", image=moon_image_url, image2=star_chart_image_url, ip=user_ip) 


if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, port=5000, threaded=True)