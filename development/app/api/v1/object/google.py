from requests import post

from classes import (
    ObjectRequest,
    GoogleVisionRequest,
    GoogleFeatureType,
    GoogleImage,
    GoogleContent,
    GoogleSource,
    GoogleFeature,
    RequestService,
)
from constants import GOOGLE_VISION_URL
from api.v1.tools.image import encode_image


def Object2GoogleVisionRequest(
    request: ObjectRequest, url_source: bool
) -> GoogleVisionRequest:

    google_features = [
        GoogleFeature(
            maxResults=request.max_objects,
            type=GoogleFeatureType.localization,
        ),
        GoogleFeature(
            maxResults=request.max_objects, type=GoogleFeatureType.label
        ),
    ]

    if url_source:
        google_image = GoogleImage(
            source=GoogleSource(imageUri=request.source)
        )
    else:
        google_image = GoogleContent(content=encode_image(request.source))

    return GoogleVisionRequest(image=google_image, features=google_features)


def handle_google_response(
    response: dict, result: dict, min_confidence: float
) -> dict:
    responses = response.get('responses')
    if not responses:
        result['error'] = 'No responses found'
        return result

    for response in responses:
        keep_response = {}
        error = False
        for annotations_name, _ in response.items():
            if annotations_name == 'error':
                error = True
                result['error'].append(response)
            else:
                for annotation in response[annotations_name]:
                    keep_response.setdefault(annotations_name, [])
                    if annotation.get('score') >= min_confidence:
                        keep_response[annotations_name].append(annotation)
        if not error:
            result['data']['objects'].append(keep_response)

    return result


def detection(
    request: ObjectRequest, settings: dict, url_source: bool
) -> dict:
    result = {}
    result['data'] = {'objects': []}
    result['error'] = []

    url = GOOGLE_VISION_URL + request.service_key
    json_request = (
        '{"requests":['
        + Object2GoogleVisionRequest(request, url_source).model_dump_json()
        + ']}'
    )
    response = post(url, json_request, timeout=10)

    result['request_id'] = request.id

    if not response.status_code == 200:
        result['error'] = response.status_code
        return result

    return handle_google_response(
        response.json(), result, request.min_confidence
    )
