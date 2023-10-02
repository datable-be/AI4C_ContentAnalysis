import json
import requests
import sys


URL = "http://0.0.0.0:8000/v1"

REQUEST = """{
  "requestType": "color",
  "data": {
    "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
    "max_colors": 3,
    "min_area": 0.15,
    "foreground_detection": true,
    "selector" : {
      "type" : "FragmentSelector",
      "conformsTo" : "http://www.w3.org/TR/media-frags/",
      "value" : "xywh=percent:87,63,9,21"
    },
    "source": "http://example.com/images/123.jpg"
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
