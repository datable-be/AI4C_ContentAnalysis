import extcolors
from typing import List, Tuple
from constants import EFT_COLORS, EFT_IDS


def detect_main_colors(
    path: str, tolerance: int
) -> Tuple[List[Tuple[Tuple[int, int, int], int]], int]:
    """
    Detects main colors from an image path and returns a list of tuples
    with RGB and pixel values, and the total pixel count,
    e.g. (((79, 79, 69), 692380), 123456789)
    Tolerance = grouping of detected colors (smaller is better, but slower)
    """

    # no limit set, this will be done after grouping
    detected_colors, total_pixel_count = extcolors.extract_from_path(
        path, tolerance=tolerance
    )

    # remove (0,0,0) background color
    for color in detected_colors:
        (rgb, _) = color
        if rgb == (0, 0, 0):
            detected_colors.remove(color)

    return (detected_colors, total_pixel_count)


def getColorName(rgb: Tuple[int, int, int]) -> str:
    """
    Match an RGB value with an EFT color name
    """
    r, g, b = rgb
    minimum = 10000
    color_name = "unknown"
    for color in EFT_COLORS:
        d = (
            abs(r - int(color["R"]))
            + abs(g - int(color["G"]))
            + abs(b - int(color["B"]))
        )
        if d <= minimum:
            minimum = d
            color_name = color["color_name"]
    return color_name


def convert_colors_to_EFT(
    colors: List[Tuple[Tuple[int, int, int], int]]
) -> List[Tuple[str, int]]:
    """
    Converts detected colors to EFT colors
    """

    result = []

    for color in colors:
        (rgb, pixels) = color
        new_color = (getColorName(rgb), pixels)
        result.append(new_color)

    return result


def merge_colors_with_threshold(
    colors: List[Tuple[str, int]], total: int, threshold: int
) -> dict:
    """
    Merge colors with the same name and return the result as percentages,
    if it exceeds the threshold.
    """

    result = {}

    for color in colors:
        (color_name, pixels) = color
        result.setdefault(color_name, 0)
        result[color_name] += pixels

    percentages = {}

    for color, pixels in result.items():
        percentage = (pixels / total) * 100
        if percentage > threshold:
            percentages[color] = percentage

    return percentages

def add_URIs(colors: dict) -> dict:
    result = {}

    for color, percentage in colors.items():
        result[color] = {}
        wikidata = None
        if EFT_IDS.get(color):
            wikidata = EFT_IDS[color]["wikidata_concept"]
        europeana = None
        if EFT_IDS.get(color):
            europeana = EFT_IDS[color]["europeana_concept"]
        result[color]["percentage"] = percentage
        result[color]["wikidata"] = wikidata
        result[color]["europeana"] = europeana

    return result

(colors, total_pixel_count) = detect_main_colors("test.jpg", 10)
eft_colors = convert_colors_to_EFT(colors)
percentages = merge_colors_with_threshold(eft_colors, total_pixel_count, 5)
result = add_URIs(percentages)
print(result)
