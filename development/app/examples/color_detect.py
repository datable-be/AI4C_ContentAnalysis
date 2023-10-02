import requests
import sys

request = """
{
  "requestType": "color",
  "data": {
    "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
    "max_colors": 3,
    "min_area": 0.15,
    "foreground_detection": TRUE,
    "selector" : {
      "type" : "FragmentSelector",
      "conformsTo" : "http://www.w3.org/TR/media-frags/",
      "value" : "xywh=percent:87,63,9,21"
    }
    "source":
"http://example.com/images/123.jpg"
  }
}
"""

response = requests.post("http://localhost:8000/v1", request)
if response.status_code == 200:
    print(response.text)
else:
    sys.exit("ERROR")
