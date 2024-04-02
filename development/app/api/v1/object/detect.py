from uuid import uuid4
from cv2.dnn import Net

from constants import APP_URL, IMAGE_DIR
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
    object_request: ObjectRequest, net: Net, settings: dict, url_source: bool
) -> dict:

    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    result = {}

    # make id if not provided
    if object_request.id == '':
        object_request.id = APP_URL + '/object-annotations/' + str(uuid4())

    # source to string
    object_request.source = str(object_request.source)

    # determine correct path for local image files
    if not url_source:
        object_request.source = f'{IMAGE_DIR}/' + object_request.source

    # internal service if key is invalid
    if object_request.service_key == '' or not object_request.service_key:
        object_request.service = RequestService.internal
        result = internal_detection(object_request, net, settings, url_source)

    if object_request.service == RequestService.googlevision:
        result = google_detection(object_request, settings, url_source)
    else:
        result = internal_detection(object_request, net, settings, url_source)

    if object_request.annotation_type == 'internal':
        return result
    else:
        return convert(result, object_request)
