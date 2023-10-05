import os
import time
from random import randint
from pathlib import Path

from fastapi import HTTPException
from numpy import asarray, ndarray
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from cv2 import imdecode, IMREAD_COLOR


def load_cv2_image_from_url(url: str, readFlag=IMREAD_COLOR) -> ndarray:
    """
    Download the image, convert it to a NumPy array, and then read
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


def sanitize_filename(string: str) -> str:
    """
    Make sure a given string is safe to use as a filename
    """

    basename = string
    extension = ""

    if "." in string:
        parts = string.split(".")
        extension = parts[-1]
        basename = "".join(parts[0: len(parts) - 1])
        for sep in ["?"]:
            extension = extension.partition(sep)[0]
        if not extension == "":
            extension = "." + extension

    b = bytes(basename, "utf-8")
    filename = b.hex()[0:10] + "_" + str(randint(0, 1000000)) + extension

    return filename


def housekeeping(path: str) -> None:
    """
    Empty a directory of files older than one day
    """

    check_file = os.path.join(path, ".housekeeping")

    # Create check_file if it does not exist
    if not os.path.exists(check_file):
        Path(check_file).touch()

    now = time.time()

    # Return if check_file is younger than one day
    if os.stat(check_file).st_mtime > now - 24 * 60 * 60:
        return None

    for filename in os.listdir(path):
        if filename == ".housekeeping":
            continue
        filepath = os.path.join(path, filename)

        # Remove if the file is older than one day
        if os.stat(filepath).st_mtime < now - 24 * 60 * 60:
            os.remove(filepath)

    # Update checkfile
    Path(check_file).touch()
