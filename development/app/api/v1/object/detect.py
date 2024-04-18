from uuid import uuid4
from cv2.dnn import Net
from transformers import BlipProcessor, BlipForQuestionAnswering

from constants import APP_URL, IMAGE_DIR, NO_OBJECTS_WARNING, TEMP_DIR
from classes import (
    ObjectRequest,
    RequestService,
    EuropeanaResponse,
    NtuaResponse,
)
from api.v1.tools.path import housekeeping
from api.v1.object.internal import detection as internal_detection
from api.v1.object.google import detection as google_detection
from api.v1.object.blipvqabase import detection as blip_detection
from api.v1.annotation.conversion import convert


def detection(
    object_request: ObjectRequest,
    net: Net,
    object_model: BlipForQuestionAnswering,
    object_processor: BlipProcessor,
    settings: dict,
    url_source: bool,
) -> dict:

    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    housekeeping(TEMP_DIR)
    result = {}

    # make id if not provided
    if object_request.id == '':
        object_request.id = APP_URL + '/' + str(uuid4())

    # source to string
    object_request.source = str(object_request.source)

    # determine correct path for local image files
    if not url_source:
        object_request.source = f'{IMAGE_DIR}/' + object_request.source

    if object_request.service == RequestService.googlevision:
        # internal service if key is invalid
        if object_request.service_key == '' or not object_request.service_key:
            object_request.service = RequestService.internal
            result = internal_detection(
                object_request, net, settings, url_source
            )
        else:
            result = google_detection(object_request, settings, url_source)
    elif object_request.service == RequestService.blipvqabase:
        result = blip_detection(
            object_request,
            object_model,
            object_processor,
            settings,
            url_source,
        )
    else:
        result = internal_detection(object_request, net, settings, url_source)

    if not result['data']['objects']:
        result.setdefault('warnings', [])
        result['warnings'].append(
            NO_OBJECTS_WARNING + f': {object_request.min_confidence}'
        )

    if object_request.annotation_type == 'internal':
        return result
    else:
        return convert(result, object_request)
