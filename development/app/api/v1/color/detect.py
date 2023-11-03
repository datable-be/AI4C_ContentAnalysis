from pathlib import Path
from cv2.dnn import Net

from api.v1.tools.color import (
    detect_main_colors,
    convert_colors_to_EFT,
    merge_colors_with_threshold_and_max,
    add_URIs,
)
from api.v1.tools.image import determine_image
from classes import ColorRequest


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
def detection(color_request: ColorRequest, net: Net, settings: dict):
    temp_path = determine_image(color_request, net, settings)

    # Detect colors
    if not temp_path:
        return {}

    (colors, total_pixel_count) = detect_main_colors(temp_path, 10)
    eft_colors = convert_colors_to_EFT(colors)
    percentages = merge_colors_with_threshold_and_max(
        eft_colors, total_pixel_count, 5, color_request.max_colors
    )
    result = add_URIs(percentages)

    # Remove tempfile
    if not settings.get("debug"):
        Path(temp_path).unlink(missing_ok=True)

    return result
