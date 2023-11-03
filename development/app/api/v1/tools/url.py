import os
from fastapi import HTTPException
from numpy import asarray, ndarray
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from cv2 import imdecode, IMREAD_COLOR

from api.v1.tools.tools import hash_object
from constants import TEMP_DIR


def load_cv2_image_from_url(url: str, readFlag=IMREAD_COLOR) -> ndarray:
    """
    Download an image, convert it to a NumPy array, and then read
    it into OpenCV format
    """
    try:
        with urlopen(url) as urlreader:
            response = urlreader.read()
    except (HTTPError, URLError) as err:
        raise HTTPException(status_code=404, detail=str(err))

    image_array = asarray(bytearray(response), dtype="uint8")
    image = imdecode(image_array, readFlag)

    return image


def url_to_tempfile(url: str) -> str:
    """
    Download an image and save it to a tempfile location
    """
    try:
        with urlopen(url) as urlreader:
            response = urlreader.read()
    except (HTTPError, URLError) as err:
        raise HTTPException(status_code=404, detail=str(err))

    basename = hash_object(url) + extension_from_url(url)
    temppath = os.path.join(TEMP_DIR, basename)

    with open(temppath, "wb") as file:
        file.write(response)

    return temppath


def extension_from_url(url: str) -> str:
    """
    Get an extension from a URL (including those with ?raw=true and such at the end))
    """

    extension = ""

    if "." in url:
        parts = url.split(".")
        extension = parts[-1]
        for sep in ["?"]:
            extension = extension.partition(sep)[0]
        if not extension == "":
            extension = "." + extension

    return extension
