from cv2 import imwrite, imread, grabCut, GC_INIT_WITH_RECT
from cv2.dnn import Net
import numpy as np

from classes import ColorRequest, ObjectRequest
from api.v1.tools.url import url_to_tempfile, url_to_temppath
from api.v1.object.internal import detection


def determine_image(color_request: ColorRequest, net: Net, settings: dict) -> str:
    """
    Determine which image to use for color detection:
        1. full image
        2. auto-crop to object
        3. crop using specified box coordinates
    Returns a path to a temporary file where the image is saved
    """

    url = str(color_request.source)

    if not color_request.foreground_detection:
        # no cropping needs to be applied
        return url_to_tempfile(url, resize_pixels=200)

    else:
        box = []
        if color_request.selector.value == "xywh=percent:0,0,100,100":
            # Use internal object detection to detect box coordinates
            # Min_confidence is set to 0.5 because default of 0.8 is too strict
            object_request = ObjectRequest(
                id=color_request.id, source=color_request.source, min_confidence=0.5
            )
            result = detection(object_request, net, settings)
            objects_found = result.get("data")
            if not objects_found:
                return url_to_tempfile(url, resize_pixels=200)
            else:
                box = objects_found[0]["box"]

        else:
            # to do: use supplied box coordinates
            box = [0, 0, 0, 0]
            pass

        return crop_image(url, box)


def crop_image(url: str, box: list) -> str:
    """
    Crop an image from URL using specified box coordinates
    and return tempfile path to cropped image
    """

    path = url_to_tempfile(url, resize_pixels=200)

    x = box[0]
    y = box[1]
    x2 = box[2]
    y2 = box[3]
    width = x2 - x
    height = y2 - y

    # Create mask
    image = imread(path)
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Define box with object
    rect = (x, y, width, height)

    # Cut and apply uniform background (which can later be removed)
    grabCut(image, mask, rect, bgdModel, fgdModel, 5, GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    image = image * mask2[:, :, np.newaxis]
    foreground_img = image.copy()
    foreground_img[np.where((mask2 == 0))] = np.array(
        [0, 0, 0]).astype("uint8")

    # Save image
    temppath = url_to_temppath(url)
    imwrite(temppath, foreground_img)

    return temppath
