import json
import requests
import sys

URL = "http://0.0.0.0:8000/v1"


REQUEST = """{
  "requestType": "object",
  "data": {
    "id": "http://example.com/images/123",
    "min_confidence": 0.8,
    "max_objects": 1,
    "source": "http://example.com/images/123.jpg",
    "service":"GoogleVision",
    "service_key":"****"
  }
}
"""


def json_pretty_print(json_string: str):
    print(json.dumps(json.loads(json_string), indent=4))


print("POST", URL)
print("REQUEST = ")
json_pretty_print(REQUEST)

response = requests.post("http://0.0.0.0:8000/v1", REQUEST)
if response.status_code == 200:
    print("RESPONSE = ")
    json_pretty_print(response.text)
else:
    sys.exit("ERROR")
