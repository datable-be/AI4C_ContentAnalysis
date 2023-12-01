from requests import post

from classes import (
    ObjectRequest,
    GoogleVisionRequest,
    GoogleFeatureType,
    GoogleImage,
    GoogleSource,
    GoogleFeature,
)
from constants import GOOGLE_VISION_URL

from api.v1.tools.tools import hash_object


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


def handle_google_response(response: dict, result: dict, min_confidence: float) -> dict:
    responses = response.get("responses")
    if not responses:
        result["error"] = "No responses found"
        return result

    for response in responses:
        keep_response = {}
        error = False
        for annotations_name, _ in response.items():
            if annotations_name == "error":
                error = True
                result["error"].append(response)
            else:
                for annotation in response[annotations_name]:
                    keep_response.setdefault(annotations_name, [])
                    if annotation.get("score") >= min_confidence:
                        keep_response[annotations_name].append(annotation)
        if not error:
            result["data"].append(keep_response)

    return result


# ObjectRequest =
#      "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
#      "min_confidence": 0.8,
#      "max_objects": 1,
#      "source": "https://cloud.google.com/vision/docs/images/bicycle_example.png",
#      "service":"GoogleVision",
#      "service_key":"****"
def detection(request: ObjectRequest, settings: dict):
    result = {}
    result["data"] = []
    result["error"] = []

    url = GOOGLE_VISION_URL + request.service_key
    json_request = (
        '{"requests":[' + Object2GoogleVisionRequest(request).model_dump_json() + "]}"
    )
    response = post(url, json_request, timeout=10)

    result["request_id"] = request.id

    if not response.status_code == 200:
        result["error"] = response.status_code
        return result

    return handle_google_response(response.json(), result, request.min_confidence)
