import string
from extcolors import extract_from_path
from typing import List, Tuple
from PIL import Image

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

    # No limit set, this will be done after grouping
    detected_colors, total_pixel_count = extract_from_path(
        path, tolerance=tolerance
    )

    # Remove (0,0,0) background color
    for color in detected_colors:
        (rgb, pixel_count) = color
        if rgb == (0, 0, 0):
            detected_colors.remove(color)
            total_pixel_count -= pixel_count

    return (detected_colors, total_pixel_count)


def getColorName(rgb: Tuple[int, int, int]) -> str:
    """
    Match an RGB value with an EFT color name
    """
    r, g, b = rgb
    minimum = 10000
    color_name = 'unknown'
    for color in EFT_COLORS:
        d = abs(r - color['R']) + abs(g - color['G']) + abs(b - color['B'])
        if d <= minimum:
            minimum = d
            color_name = color['color_name']
    color_name = color_name.lower()
    return color_name


def convert_colors_to_EFT(
    colors: List[Tuple[Tuple[int, int, int], int]],
) -> List[Tuple[str, int]]:
    """
    Converts detected colors to Europeana Fashion Thesaurus colors
    """

    result = []

    for color in colors:
        (rgb, pixels) = color
        new_color = (getColorName(rgb), pixels)
        result.append(new_color)

    return result


def merge_colors_with_threshold_and_max(
    colors: List[Tuple[str, int]], total: int, threshold: float, max: int
) -> dict:
    """
    Merge colors with the same name and return the result as percentages,
    if it exceeds the threshold. Apply max colors parameter.
    (Note: this function does several things at once for efficiency)
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

    sorted_percentages = sorted(
        percentages.items(), key=lambda x: x[1], reverse=True
    )

    sorted_percentages = sorted_percentages[0:max]

    sorted_result = {k: v for k, v in sorted_percentages}

    return sorted_result


def add_URIs(colors: dict) -> dict:
    """
    Add Wikidata and Europeana URIs to the color names
    """
    result = {}

    for color, percentage in colors.items():
        result[color] = {}
        wikidata = None
        europeana = None
        wikidata_uri = None
        europeana_uri = None
        if EFT_IDS.get(color):
            wikidata = EFT_IDS[color]['wikidata_concept']
            europeana = EFT_IDS[color]['europeana_concept']
            wikidata_uri = EFT_IDS[color]['wikidata_concepturi']
            europeana_uri = EFT_IDS[color]['europeana_concepturi']
        result[color]['percentage'] = percentage
        result[color]['wikidata'] = wikidata
        result[color]['europeana'] = europeana
        result[color]['wikidata_uri'] = wikidata_uri
        result[color]['europeana_uri'] = europeana_uri

    return result


def extract_colors_from_sentence(sentence: str) -> List[str]:
    """
    Extract EFT colors from a sentence
    """
    result = []

    sentence = sentence.lower()
    for char in string.punctuation:
        sentence = sentence.replace(char, '')

    words = sentence.split(' ')

    result = list(set([word for word in words if word in EFT_IDS]))

    return result


def is_quasi_monochrome_with_rgb(image_path: str) -> bool:
    """
    Determine whether an image is monochrome with an RGB channel
    or a color image containing a black and white photo
    """
    image = Image.open(image_path)

    # Check if the image has an RGB channel
    bands = image.getbands()
    if (
        len(bands) != 3
        or 'R' not in bands
        or 'G' not in bands
        or 'B' not in bands
    ):
        return False

    # Check if the image contains a black and white photo
    num_pixels = 0
    if image.mode == 'RGBA':
        # Split image into separate channels
        r, g, b, a = image.split()

        # Check if the alpha channel is mostly white
        alpha_pixels = a.getdata()
        num_white_pixels = sum(1 for pixel in alpha_pixels if pixel == 255)
        num_pixels = len(alpha_pixels)
        if num_white_pixels / num_pixels > 0.99:
            return True

    # Check if the image is monochrome
    if image.mode == 'L':
        return True

    # Check if the image is RGB but with only one color channel
    if image.mode == 'RGB':
        r, g, b = image.split()
        if r.getextrema() == g.getextrema() == b.getextrema():
            return True
        # Check if the image has very low color saturation
        hsv_image = image.convert('HSV')
        h, s, v = hsv_image.split()
        s_pixels = s.getdata()
        if num_pixels == 0:
            num_pixels = len(s_pixels)
        num_low_sat_pixels = sum(1 for pixel in s_pixels if pixel < 32)
        if num_low_sat_pixels / num_pixels > 0.95:
            return True

    return False
