from cv2 import imwrite, imread, grabCut, GC_INIT_WITH_RECT
from cv2.dnn import Net
import numpy as np

from classes import ColorRequest, ObjectRequest
from api.v1.tools.url import (
    url_to_tempfile,
    url_to_temppath,
    load_cv2_image_from_url,
)
from api.v1.object.internal import detection


def determine_image(
    color_request: ColorRequest, net: Net, settings: dict, resize: int | None
) -> str:
    """
    Determine which image to use for color detection:
        1. full image
        2. auto-crop to object
        3. crop using specified box coordinates
    Returns a path to a temporary file where the image is saved
    """

    url = str(color_request.source)

    if not color_request.foreground_detection:
        # No cropping needs to be applied
        return url_to_tempfile(url, resize_pixels=resize)

    else:
        if color_request.selector.value == 'xywh=percent:0,0,100,100':
            # Use internal object detection to detect box coordinates
            # Min_confidence is set to 0.5 because default of 0.8 is too strict
            object_request = ObjectRequest(
                id=color_request.id,
                source=color_request.source,
                min_confidence=0.5,
            )
            result = detection(object_request, net, settings)
            objects_found = result.get('data')
            if not objects_found:
                return url_to_tempfile(url, resize_pixels=200)
            else:
                box = objects_found[0].get('box_px')
                return crop_image(url, box, resize, mode='px', foreground=True)

        else:
            # Use supplied box coordinates
            box = [
                int(x)
                for x in color_request.selector.value.partition('percent:')[
                    2
                ].split(',')
            ]
            return crop_image(url, box, resize, mode='pc', foreground=False)


def crop_image(
    url: str,
    box: list[int],
    resize_pixels: int | None,
    mode: str,
    foreground: bool,
) -> str:
    """
    Crop an image from URL using specified box coordinates
    and return tempfile path to cropped image
    """

    image = load_cv2_image_from_url(url, resize_pixels=resize_pixels)

    # Convert box percentages to box coordinates

    height = image.shape[0]
    width = image.shape[1]

    if mode == 'pc':
        x = int(width * box[0] / 100)
        y = int(height * box[1] / 100)
        x2 = int(width * box[2] / 100)
        y2 = int(height * box[3] / 100)
        box = [x, y, x2, y2]

    if foreground:
        # Create mask
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        # Cut and apply uniform background (which can later be removed)
        grabCut(image, mask, box, bgdModel, fgdModel, 5, GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        image = image * mask2[:, :, np.newaxis]
        cropped_image = image.copy()
        cropped_image[np.where((mask2 == 0))] = np.array([0, 0, 0]).astype(
            'uint8'
        )
    else:
        cropped_image = image[box[1] : box[3], box[0] : box[2]]

    # Save image
    temppath = url_to_temppath(url)
    imwrite(temppath, cropped_image)

    return temppath
