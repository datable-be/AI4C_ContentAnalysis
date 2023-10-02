import requests
import sys

request = """
{
  "requestType": "object",
  "data": {
    "id": "http://example.com/images/123",
    "min_confidence": 0.8,
    "max_objects": 1,
    "source":
"http://example.com/images/123.jpg",
    "service":"GoogleVision",
    "service_key":"****"
  }
}
"""

response = requests.post("http://localhost:8000/v1", request)
if response.status_code == 200:
    print(response.text)
else:
    sys.exit("ERROR")
