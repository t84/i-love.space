from flask import Flask, render_template, request, jsonify
import requests, base64
from datetime import datetime, timedelta
from flask_caching import Cache
from bs4 import BeautifulSoup


apikey_geoapify = "49be3a765aa44ec1a02e6baddcaaeb50"
apikey_nasa = "Ah6cxAedN8mGI9jddu1hhZpLufc036UZE7J6AaBQ"


app = Flask(__name__)


DEVELOPMENT_ENV = False


cache = Cache(app, config={'CACHE_TYPE': 'simple'})

YYYY_MM_DD = datetime.now().strftime("%Y-%m-%d")


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/api/iss')
def iss():
        try:
            cached_iss_response = cache.get('update_iss_response')
            if cached_iss_response:
                r = requests.get('https://api.wheretheiss.at/v1/satellites/25544')
                if r.status_code == 200:
                    r = r.json()
                    cached_iss_response['data']['coordinates']['latitude'] = r['latitude']
                    cached_iss_response['data']['coordinates']['longitude'] = r['longitude']

                    cache.set('update_iss_response', cached_iss_response, timeout=10)

                    return jsonify(cached_iss_response)
                else:
                    return jsonify({"message":"error", "error": "Error with API"})

            r = requests.get('https://api.wheretheiss.at/v1/satellites/25544')
            if r.status_code == 200:

                r = r.json()

                headers = {
                    'User-Agent': 'https://i-love.space',
                    'Referer': 'https://i-love.space',  
                }
                url = f"https://api.geoapify.com/v1/geocode/reverse?lat={r['latitude']}&lon={r['longitude']}&apiKey={apikey_geoapify}"
                r2 = requests.get(url, headers=headers).json()        
                try:
                    country_name = r2['features'][0]['properties']['name']
                except:
                    country_name = r2['features'][0]['properties']['country']

                response_data = {"data": {"coordinates": {"latitude": r['latitude'], "longitude": r['longitude']}, "country_name": country_name}}

                cache.set('update_iss_response', response_data, timeout=10)

                return jsonify(response_data)

            else:
                return jsonify({"message":"error", "error": "Error with API"})
        except Exception as e:
            print(e)
            return jsonify({"message": "error", "error": "Error with API"})



@app.route('/api/apod', methods=['GET'])
def apod():
    try:
        tomorrow = datetime.now() + timedelta(days=1)  
        midnight = datetime.combine(tomorrow, datetime.min.time())
        now = datetime.now()
        time_until_tmr_in_seconds = int((midnight - now).total_seconds())

        
        cached_data = cache.get("apod")
        today_date = datetime.now().date().isoformat()

        if cached_data and cached_data.get('date') == today_date:
            time_until_reset = time_until_tmr_in_seconds
            return jsonify({"message": "success", "data": cached_data, "time_until_reset": time_until_reset})
        else:
            r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apikey_nasa}&date={today_date}")
            print(r.status_code)
            if r.status_code == 200:
                json_apod = r.json()

                date = json_apod['date']
                author = json_apod.get('copyright', 'N/A')
                title = json_apod['title']
                description = json_apod['explanation']
                hdimage = json_apod.get('hdurl', '')
                image = json_apod['url']

                data = {
                    "date": date,
                    "author": author,
                    "title": title,
                    "description": description,
                    "images": {
                        "hdimage": hdimage,
                        "image": image
                    }
                }

                cache.set("apod", data, timeout=time_until_tmr_in_seconds)

                return jsonify({"message": "success", "data": data, "time_until_reset": time_until_tmr_in_seconds})
            else:
                return jsonify({"message": "error", "error": "Error with API"})
    except Exception as e:
        print(e)
        return jsonify({"message": "error", "error": "Error with API"})

@app.route('/api/peopleinspace', methods=['GET'])
def peopleinspace():
        try:
            cached_peopleinspace_response = cache.get('peopleinspace')
            if cached_peopleinspace_response:
                return cached_peopleinspace_response
            else:
                r = requests.get("http://api.open-notify.org/astros.json").json()

                if r["message"] == "success":
                    people = r["people"]

                    people_list = []

                    for person in people:
                        person_info = {
                            "name": person['name'],
                            "craft": person['craft']
                        }
                        people_list.append(person_info)

                    cache.set("peopleinspace", {"message":"success", "people": people_list}, timeout=1800)

                    return jsonify({"message":"success", "people": people_list})

                else:
                    return jsonify({"message":"error", "error": "Error with API"})
        except Exception as e:
            print(e)
            return jsonify({"message": "error", "error": "Error with API"})

#@app.route('/api/solarstorm', methods=['GET'])
#def solarstorm():
#        try:
#            data = requests.get("https://services.swpc.noaa.gov/products/noaa-scales.json")
#
#            if data.status_code == 200:
#
#                data = data.json()
#
#                solar_storms = []
#
#                for key, entry in data.items():
#                    date_stamp = entry['DateStamp']
#                    time_stamp = entry['TimeStamp']
#
#                    if entry['S']['Prob'] is not None:
#                        prob_solar_storm = float(entry['S']['Prob'])
#                        if prob_solar_storm.is_integer():
#                            prob_solar_storm = int(prob_solar_storm)
#                        solar_storms.append({
#                            "date_stamp": date_stamp,
#                            "time_stamp": time_stamp,
#                            "probability": prob_solar_storm
#                        })
#                    else:
#                        solar_storms.append({
#                            "date_stamp": date_stamp,
#                            "time_stamp": time_stamp,
#                            "probability": None
#                        })
#
#                return jsonify({"message":"success", "solar_storms": solar_storms})
#            else:
#                return jsonify({"message":"error", "error": "Error with API"})
#        except Exception as e:
#            print(e)
#            return jsonify({"message": "error", "error": "Error with API"})

@app.route('/api/exoplanets', methods=['GET'])
def exoplanets():
        try:
            response = requests.get("https://www.openexoplanetcatalogue.com/")
            if response.status_code == 200:
            
                soup = BeautifulSoup(response.content, "html.parser")

                table = soup.find("table", {"summary": "Statistics"})

                data = {}

                data = {}

                for row in table.find_all("tr"):
                    columns = row.find_all(["th", "td"])
                    key = columns[0].get_text(strip=True)
                    value = columns[1].get_text(strip=True)

                    # Clean the key
                    key = key.replace(" ", "_").split("(")[0].strip().casefold()

                    # Exclude the "list_of_contributors" key
                    if key != "list_of_contributors":
                        data[key] = value


                data["credit"] = "https://www.openexoplanetcatalogue.com/"

                return jsonify({"message": "success", "data": data})
            else:
                return jsonify({"message":"error", "error": "Error with API"})
        except Exception as e:
            print(e)
            return jsonify({"message": "error", "error": "Error with API"})
        
@app.route('/api/solarsystem', methods=['GET'])
def solarsystem():
    try:
        cached_iss_response = cache.get('solarsystem')
        if cached_iss_response:
            return jsonify(cached_iss_response)
        else:
            response = requests.get("https://api.le-systeme-solaire.net/rest.php/knowncount?rowData=true")
            if response.status_code == 200:
                response_json = response.json()
                data = [{"id": item[0], "count": item[1], "last_updated": datetime.strptime(item[2], "%d/%m/%Y").strftime("%m/%d/%Y")} for item in response_json["knowncount"]["records"]]

                current_epoch_time = int(datetime.now().timestamp())

                data = {"message": "success", "last_cached": current_epoch_time, "data": data}

                cache.set('solarsystem', data, timeout=3600)

                return jsonify(data)
            else:
                return jsonify({"message": "error", "error": "Error with API"})
    except Exception as e:
        print(e)
        return jsonify({"message": "error", "error": "Error with API"})

        
if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV, port=5000, threaded=True)
