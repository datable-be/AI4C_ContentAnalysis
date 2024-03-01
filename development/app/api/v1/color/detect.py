from cv2.dnn import Net
from transformers import BlipProcessor, BlipForQuestionAnswering

from api.v1.color.internal import detection as internal_detection
from api.v1.color.huggingface import detection as huggingface_detection
from classes import ColorRequest, RequestService

MODEL_RESPONSE = {
    "@context": "...",
    "@graph": [
        {
            "id": "http://datable.be/object-annotations/123",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_object-detector",
                "type": "Software",
                "name": "AI4C object detector",
            },
            "body": {
                "source": "http://www.wikidata.org/entity/Q200539",
                "type": "SpecificResource",
                "purpose": "tagging",
            },
            "target": {
                "source": "http://example.com/image123.jpg",
                "type": "Image",
                "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
                "selector": {
                    "type": "FragmentSelector",
                    "conformsTo": "http://www.w3.org/TR/media-frags/",
                    "value": "xywh=percent:10,20,5,14",
                },
            },
            "confidence": 0.8,
        },
        {
            "id": "http://datable.be/object-annotations/456",
            "type": "Annotation",
            "created": "2023-09-30",
            "creator": {
                "id": "https://github.com/hvanstappen/AI4C_object-detector",
                "type": "Software",
                "name": "AI4C object detector",
            },
            "body": {
                "source": "http://www.wikidata.org/entity/Q80151",
                "type": "SpecificResource",
                "purpose": "tagging",
            },
            "target": {
                "source": "http://example.com/image123.jpg",
                "type": "Image",
                "id": "http://mint-projects.image.ntua.gr/europeana-fashion/500208081",
                "selector": {
                    "type": "FragmentSelector",
                    "conformsTo": "http://www.w3.org/TR/media-frags/",
                    "value": "xywh=percent:87,63,9,21",
                },
            },
            "confidence": 0.7,
        },
    ],
}


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
) -> dict:
    if settings.get("dummy"):
        return MODEL_RESPONSE

    if color_request.service == RequestService.internal:
        return internal_detection(color_request, net, settings)

    elif color_request.service == RequestService.huggingface:
        return huggingface_detection(
            color_request, color_model, color_processor, settings
        )
