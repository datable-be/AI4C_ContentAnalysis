from cv2.dnn import Net

from classes import (
    ObjectRequest,
    RequestService,
    EuropeanaResponse,
    NtuaResponse,
)
from api.v1.object.internal import detection as internal_detection
from api.v1.object.google import detection as google_detection
from api.v1.annotation.conversion import convert


def detection(
    object_request: ObjectRequest, net: Net, settings: dict
) -> dict | EuropeanaResponse | NtuaResponse:

    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    result = {}

    # internal service if key is invalid
    if object_request.service_key == '' or not object_request.service_key:
        object_request.service = RequestService.internal
        result = internal_detection(object_request, net, settings)

    if object_request.service == RequestService.googlevision:
        result = google_detection(object_request, settings)
    else:
        result = internal_detection(object_request, net, settings)

    if object_request.annotation_type == 'internal':
        return result
    else:
        return convert(result, object_request)
