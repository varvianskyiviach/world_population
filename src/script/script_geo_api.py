import json

import requests

from config.settings import API_URL, FILE_JSON_PATH, PARAMS

resp = requests.get(url=API_URL, params=PARAMS)
data = resp.json()

with open(f"{FILE_JSON_PATH}", "w") as file:
    file.write(json.dumps(data))
