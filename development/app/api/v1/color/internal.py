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


def detection(
    color_request: ColorRequest, net: Net, settings: dict, url_source: bool
) -> dict:
    result = {}
    color_request.source = str(color_request.source)

    temp_path = determine_image(color_request, net, settings, 200, url_source)

    # Detect colors
    if not temp_path:
        return result

    (colors, total_pixel_count) = detect_main_colors(temp_path, 10)
    eft_colors = convert_colors_to_EFT(colors)
    percentages = merge_colors_with_threshold_and_max(
        eft_colors, total_pixel_count, 5, color_request.max_colors
    )
    result['colors'] = add_URIs(percentages)

    # Remove tempfile
    if settings.get('debug'):
        basename = Path(temp_path).name
        url = (
            settings['host']
            + ':'
            + str(settings['port'])
            + '/image?img='
            + basename
        )
        result['cropped_image'] = url
    else:
        Path(temp_path).unlink(missing_ok=True)

    return result
