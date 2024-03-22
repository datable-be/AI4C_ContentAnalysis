import json
import requests
import sys

URL = 'http://0.0.0.0:8000/v1/object'

EXAMPLES = {
    'bicycle': 'https://cloud.google.com/vision/docs/images/bicycle_example.png'
}

with open(
    '/home/tdeneire/Dropbox/code/python/AI4C/doc/google-api/key', 'r'
) as reader:
    KEY = reader.read().strip()

REQUEST = f"""{{
    "min_confidence": 0.9,
    "max_objects": 3,
    "source":"https://cloud.google.com/vision/docs/images/bicycle_example.png",
    "service":"GoogleVision",
    "service_key":"{KEY}",
    "annotation_type": "internal"
}}
"""


def json_pretty_print(json_string: str):
    print(json.dumps(json.loads(json_string), indent=4))


print('POST', URL)
print('REQUEST = ')
json_pretty_print(REQUEST)

response = requests.post(URL, REQUEST, timeout=10)
if response.status_code == 200:
    print('RESPONSE = ')
    json_pretty_print(response.text)
else:
    sys.exit('ERROR = ' + response.text)
