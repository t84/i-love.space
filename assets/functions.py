import os
import requests
import hashlib
import base64
from datetime import datetime

api_key = "28662158-d89a-4a27-a202-0584ee64e9cf:ecf887cc93015e93ba12e7deec48f22837cdab04b352f4a60ce7e7c748c84e92b8ad0120944c8c1a16b28c50b9effbd626e57cdfdf6b74dac368814da98ebdfdac392c47290de1ddfc96ed3fe94e68ef2961c30ba3e292107ca1da2c4e99e4328396a0c2fbb98c2bb5f402c96ef08eb9"
constellations = [
    {"abbr": "and", "name": "Andromeda"},
    {"abbr": "leo", "name": "Leo"},
    {"abbr": "ant", "name": "Antlia"},
    {"abbr": "lmi", "name": "Leo Minor"},
    {"abbr": "aps", "name": "Apus"},
    {"abbr": "lep", "name": "Lepus"},
    {"abbr": "aqr", "name": "Aquarius"},
    {"abbr": "lib", "name": "Libra"},
    {"abbr": "aql", "name": "Aquila"},
    {"abbr": "lup", "name": "Lupus"},
    {"abbr": "ara", "name": "Ara"},
    {"abbr": "lyn", "name": "Lynx"},
    {"abbr": "ari", "name": "Aries"},
    {"abbr": "lyr", "name": "Lyra"},
    {"abbr": "aur", "name": "Auriga"},
    {"abbr": "men", "name": "Mensa"},
    {"abbr": "boo", "name": "Boötes"},
    {"abbr": "mic", "name": "Microscopium"},
    {"abbr": "cae", "name": "Caelum"},
    {"abbr": "mon", "name": "Monoceros"},
    {"abbr": "cam", "name": "Camelopardalis"},
    {"abbr": "mus", "name": "Musca"},
    {"abbr": "cnc", "name": "Cancer"},
    {"abbr": "nor", "name": "Norma"},
    {"abbr": "cvn", "name": "Canes Venatici"},
    {"abbr": "oct", "name": "Octans"},
    {"abbr": "cma", "name": "Canis Major"},
    {"abbr": "oph", "name": "Ophiuchus"},
    {"abbr": "cmi", "name": "Canis Minor"},
    {"abbr": "ori", "name": "Orion"},
    {"abbr": "cap", "name": "Capricornus"},
    {"abbr": "pav", "name": "Pavo"},
    {"abbr": "car", "name": "Carina"},
    {"abbr": "peg", "name": "Pegasus"},
    {"abbr": "cas", "name": "Cassiopeia"},
    {"abbr": "per", "name": "Perseus"},
    {"abbr": "cen", "name": "Centaurus"},
    {"abbr": "phe", "name": "Phoenix"},
    {"abbr": "cep", "name": "Cepheus"},
    {"abbr": "pic", "name": "Pictor"},
    {"abbr": "cet", "name": "Cetus"},
    {"abbr": "psc", "name": "Pisces"},
    {"abbr": "cha", "name": "Chamaeleon"},
    {"abbr": "psa", "name": "Piscis Austrinus"},
    {"abbr": "cir", "name": "Circinus"},
    {"abbr": "pup", "name": "Puppis"},
    {"abbr": "col", "name": "Columba"},
    {"abbr": "pyx", "name": "Pyxis"},
    {"abbr": "com", "name": "Coma Berenices"},
    {"abbr": "ret", "name": "Reticulum"},
    {"abbr": "cra", "name": "Corona Australis"},
    {"abbr": "sge", "name": "Sagitta"},
    {"abbr": "crb", "name": "Corona Borealis"},
    {"abbr": "sgr", "name": "Sagittarius"},
    {"abbr": "crv", "name": "Corvus"},
    {"abbr": "sco", "name": "Scorpius"},
    {"abbr": "crt", "name": "Crater"},
    {"abbr": "scl", "name": "Sculptor"},
    {"abbr": "cru", "name": "Crux"},
    {"abbr": "sct", "name": "Scutum"},
    {"abbr": "cyg", "name": "Cygnus"},
    {"abbr": "ser", "name": "Serpens"},
    {"abbr": "del", "name": "Delphinus"},
    {"abbr": "dor", "name": "Dorado"},
    {"abbr": "sex", "name": "Sextans"},
    {"abbr": "dra", "name": "Draco"},
    {"abbr": "tau", "name": "Taurus"},
    {"abbr": "equ", "name": "Equuleus"},
    {"abbr": "tel", "name": "Telescopium"},
    {"abbr": "eri", "name": "Eridanus"},
    {"abbr": "tri", "name": "Triangulum"},
    {"abbr": "for", "name": "Fornax"},
    {"abbr": "tra", "name": "Triangulum Australe"},
    {"abbr": "gem", "name": "Gemini"},
    {"abbr": "tuc", "name": "Tucana"},
    {"abbr": "gru", "name": "Grus"},
    {"abbr": "uma", "name": "Ursa Major"},
    {"abbr": "her", "name": "Hercules"},
    {"abbr": "umi", "name": "Ursa Minor"},
    {"abbr": "hor", "name": "Horologium"},
    {"abbr": "vel", "name": "Vela"},
    {"abbr": "hya", "name": "Hydra"},
    {"abbr": "vir", "name": "Virgo"},
    {"abbr": "hyi", "name": "Hydrus"},
    {"abbr": "vol", "name": "Volans"},
    {"abbr": "ind", "name": "Indus"},
    {"abbr": "vul", "name": "Vulpecula"},
    {"abbr": "lac", "name": "Lacerta"}
]


def get_location(ip):
    return requests.get(f"http://ip-api.com/json/{ip}").json()

def get_moon_phase(data):
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
    response = requests.post('https://api.astronomyapi.com/api/v2/studio/moon-phase', headers=headers, json=json_data).json()
    return response['data']['imageUrl']

def get_star_chart(constellation, data):
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
                "constellation": constellation
            }
        }
    }
    response = requests.post('https://api.astronomyapi.com/api/v2/studio/star-chart', headers=headers, json=json_data).json()
    print(response)
    return response['data']['imageUrl']