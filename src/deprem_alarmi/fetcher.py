import requests

USGS_URL = r"https://earthquake.usgs.gov/fdsnws/event/1/query"

PARAMS = {
    "format": "geojson",
    "minlatitude": 36,
    "maxlatitude": 42,
    "minlongitude": 26,
    "maxlongitude": 45,
    "orderby": "time",
}

def fetch_earthquakes():
    r = requests.get(USGS_URL, params=PARAMS, timeout=10)
    r.raise_for_status()
    return r.json()
