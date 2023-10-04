import json
import requests
import sys

URL = "http://0.0.0.0:8000/v1/object"


REQUEST = """{
    "id": "http://example.com/images/123",
    "min_confidence": 0.8,
    "max_objects": 1,
    "source": "https://github.com/datable-be/AI4C_ContentAnalysis/blob/da9995b6a2a2795bb2d2cce0695417efc5b674f3/scripts/color-detector/examples/39355scr_0ed48a9fe99bfe5_e183b86fc24d9855178e546b5f96c28a.jpg?raw=true",
    "service":"internal",
    "service_key":"****"
}
"""


def json_pretty_print(json_string: str):
    print(json.dumps(json.loads(json_string), indent=4))


print("POST", URL)
print("REQUEST = ")
json_pretty_print(REQUEST)

response = requests.post(URL, REQUEST)
if response.status_code == 200:
    print("RESPONSE = ")
    json_pretty_print(response.text)
else:
    sys.exit("ERROR = " + response.text)
