from uuid import uuid4
from cv2.dnn import Net
from transformers import BlipProcessor, BlipForQuestionAnswering

from constants import APP_URL, IMAGE_DIR, NO_COLORS_WARNING, TEMP_DIR
from api.v1.color.internal import detection as internal_detection
from api.v1.color.blipvqabase import detection as blipvqabase_detection
from api.v1.annotation.conversion import convert
from api.v1.tools.path import housekeeping
from classes import (
    ColorRequest,
    RequestService,
    EuropeanaResponse,
    NtuaResponse,
)


def detection(
    color_request: ColorRequest,
    net: Net,
    color_model: BlipForQuestionAnswering,
    color_processor: BlipProcessor,
    settings: dict,
    url_source: bool,
) -> dict:

    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    housekeeping(TEMP_DIR)
    result = {}

    # make id if not provided
    if color_request.id == '':
        color_request.id = APP_URL + '/' + str(uuid4())

    # source to string
    color_request.source = str(color_request.source)

    # determine correct path for local image files
    if not url_source:
        color_request.source = f'{IMAGE_DIR}/' + color_request.source

    if color_request.service == RequestService.internal:
        result = internal_detection(color_request, net, settings, url_source)

    elif color_request.service == RequestService.blipvqabase:
        result = blipvqabase_detection(
            color_request,
            net,
            color_model,
            color_processor,
            settings,
            url_source,
        )

    if not result['data']['colors']:
        result.setdefault('warnings', [])
        result['warnings'].append(
            NO_COLORS_WARNING + f': {color_request.min_area}'
        )

    if color_request.annotation_type == 'internal':
        return result
    else:
        return convert(result, color_request)
