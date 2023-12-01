import requests
from json import dumps

from classes import (
    ObjectRequest,
    GoogleVisionRequest,
    GoogleFeatureType,
    GoogleImage,
    GoogleSource,
    GoogleFeature,
)
from constants import GOOGLE_VISION_URL


def Object2GoogleVisionRequest(object_request: ObjectRequest) -> GoogleVisionRequest:
    google_source = GoogleSource(imageUri=object_request.source)
    google_image = GoogleImage(source=google_source)
    google_features = [
        GoogleFeature(
            maxResults=object_request.max_objects, type=GoogleFeatureType.localization
        ),
        GoogleFeature(
            maxResults=object_request.max_objects, type=GoogleFeatureType.label
        ),
    ]
    return GoogleVisionRequest(image=google_image, features=google_features)


# ObjectRequest =
#      "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
#      "min_confidence": 0.8,
#      "max_objects": 1,
#      "source": "https://cloud.google.com/vision/docs/images/bicycle_example.png",
#      "service":"GoogleVision",
#      "service_key":"****"
def detection(object_request: ObjectRequest, settings: dict):
    result = {}
    url = GOOGLE_VISION_URL + object_request.service_key
    request = (
        '{"requests":['
        + Object2GoogleVisionRequest(object_request).model_dump_json()
        + "]}"
    )
    response = requests.post(url, request, timeout=10)
    print(response.text)
    # handle confidence settings!
    if response.status_code == 200:
        print("RESPONSE = ")
        result["data"] = response.json()
    else:
        result["error"] = response.status_code
    return result
