import requests
import sys

response = requests.post("http://localhost:8000/v1/object/detect", {})
if response.status_code == 200:
    print(response.text)
else:
    sys.exit("ERROR")
