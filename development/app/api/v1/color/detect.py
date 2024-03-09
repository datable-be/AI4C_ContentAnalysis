from cv2.dnn import Net
from transformers import BlipProcessor, BlipForQuestionAnswering

from api.v1.color.internal import detection as internal_detection
from api.v1.color.huggingface import detection as huggingface_detection
from api.v1.annotation.conversion import convert
from classes import (
    ColorRequest,
    RequestService,
    EuropeanaResponse,
    NtuaResponse,
)

#  ColorRequest =
#  {
#      "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
#      "max_colors": 3,
#      "min_area": 0.15,
#      "foreground_detection": true,
#      "selector" : {
#        "type" : "FragmentSelector",
#        "conformsTo" : "http://www.w3.org/TR/media-frags/",
#        "value" : "xywh=percent:87,63,9,21"
#      },
#      "source": "http://example.com/images/123.jpg"
#    }
def detection(
    color_request: ColorRequest,
    net: Net,
    color_model: BlipForQuestionAnswering,
    color_processor: BlipProcessor,
    settings: dict,
) -> dict | EuropeanaResponse | NtuaResponse:

    if settings.get('dummy'):
        from constants import MODEL_RESPONSE

        return MODEL_RESPONSE

    result = {}

    if color_request.service == RequestService.internal:
        result = internal_detection(color_request, net, settings)

    elif color_request.service == RequestService.huggingface:
        result = huggingface_detection(
            color_request, net, color_model, color_processor, settings
        )

    if color_request.annotation_type == 'internal':
        return result
    else:
        return convert(result, color_request)
