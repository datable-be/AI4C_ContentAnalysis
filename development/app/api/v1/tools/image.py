import cv2 as cv
import numpy as np
from random import randint
import os

from constants import TEMP_DIR


def crop_image(path: str, box: list) -> str:
    """
    Crop an image from URL using specified box coordinates
    and return tempfile path to cropped image
    """
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
