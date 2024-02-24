from pathlib import Path
from cv2.dnn import Net

from api.v1.tools.color import (
    detect_main_colors,
    convert_colors_to_EFT,
    merge_colors_with_threshold_and_max,
    add_URIs,
)
from api.v1.tools.image import determine_image
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
def detection(color_request: ColorRequest, net: Net, settings: dict) -> dict:
    if settings.get("dummy"):
        return MODEL_RESPONSE

    result = {}

    if color_request.service == RequestService.internal:
        temp_path = determine_image(color_request, net, settings)

        # Detect colors
        if not temp_path:
            return result

        (colors, total_pixel_count) = detect_main_colors(temp_path, 10)
        eft_colors = convert_colors_to_EFT(colors)
        percentages = merge_colors_with_threshold_and_max(
            eft_colors, total_pixel_count, 5, color_request.max_colors
        )
        result = add_URIs(percentages)

        # Remove tempfile
        if settings.get("debug"):
            basename = Path(temp_path).name
            url = (
                settings["host"]
                + ":"
                + str(settings["port"])
                + "/image?img="
                + basename
            )
            result["cropped_image"] = url
        else:
            Path(temp_path).unlink(missing_ok=True)

    elif color_request.service == RequestService.huggingface:
        # to do (including example and documenation!)
        pass

    return result
