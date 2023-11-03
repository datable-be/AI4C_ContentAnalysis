import cv2 as cv
import numpy as np
from random import randint
import os

from constants import TEMP_DIR
from classes import ColorRequest, ObjectRequest
from api.v1.tools.url import url_to_tempfile
from api.v1.object.internal import detection


def determine_image(
    color_request: ColorRequest, net: cv.dnn.Net, settings: dict
) -> str:
    url = str(color_request.source)

    if not color_request.foreground_detection:
        # no cropping needs to be applied
        return url_to_tempfile(url)

    else:
        box = []
        if color_request.selector.value == "xywh=percent:0,0,100,100":
            # use internal object detection to detect box coordinates
            # min_confidence is set to 0.5 because default of 0.8 is too strict
            object_request = ObjectRequest(
                id=color_request.id, source=color_request.source, min_confidence=0.5
            )
            result = detection(object_request, net, settings)
            objects_found = result.get("data")
            if not objects_found:
                return url_to_tempfile(url)
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

    path = url_to_tempfile(url)

    x = box[0]
    y = box[1]
    x2 = box[2]
    y2 = box[3]
    width = x2 - x
    height = y2 - y

    # create mask
    image = cv.imread(path)
    mask = np.zeros(image.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # define box with object
    rect = (x, y, width, height)

    # remove background
    # to do: this hangs for image https://github.com/datable-be/AI4C_colordetector/blob/main/examples/RS41124_T3796_0004-hpr_8_enhanced.jpg?raw=true
    cv.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")
    image = image * mask2[:, :, np.newaxis]

    foreground_img = image.copy()
    foreground_img[np.where((mask2 == 0))] = np.array([0, 0, 0]).astype(
        "uint8"
    )  # this allows you to change the background color after grabcut

    basename = str(randint(0, 1000000)) + os.path.basename(path)
    tempfile = os.path.join(TEMP_DIR, basename)
    cv.imwrite(tempfile, foreground_img)

    return tempfile
