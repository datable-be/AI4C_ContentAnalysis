from pathlib import Path
from cv2.dnn import Net

from api.v1.tools.color import (
    detect_main_colors,
    convert_colors_to_EFT,
    merge_colors_with_threshold_and_max,
    add_URIs,
)
from api.v1.tools.image import determine_image
from api.v1.tools.path import filename_to_url
from api.v1.tools.color import is_image_monochrome
from classes import ColorRequest
from constants import BW_WARNING


def detection(
    request: ColorRequest, net: Net, settings: dict, url_source: bool
) -> dict:
    result = {}
    request.source = str(request.source)

    temp_path = determine_image(request, net, settings, 200, url_source)
    if not temp_path:
        return result

    if is_image_monochrome(temp_path):
        result.setdefault('warnings', [])
        result['warnings'].append(BW_WARNING)

    # Detect colors

    (colors, total_pixel_count) = detect_main_colors(temp_path, 10)
    eft_colors = convert_colors_to_EFT(colors)
    threshold = request.min_area * 100
    percentages = merge_colors_with_threshold_and_max(
        eft_colors, total_pixel_count, threshold, request.max_colors
    )
    result['data'] = {'colors': add_URIs(percentages)}

    # Add image link
    basename = Path(temp_path).name
    result['data']['cropped_image'] = filename_to_url(basename)

    result['request_id'] = request.id
    result['source'] = request.source

    return result
