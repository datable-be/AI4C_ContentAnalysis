from os.path import join
from fastapi import HTTPException
from numpy import asarray, ndarray
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from cv2 import imdecode, imwrite, resize, IMREAD_COLOR, INTER_LINEAR

from api.v1.tools.tools import hash_object
from constants import TEMP_DIR


def resize_image(image: ndarray, pixels: int):
    if image.shape[1] < image.shape[0]:
        scale_factor = pixels / image.shape[1]
    else:
        scale_factor = pixels / image.shape[0]
    W = int(image.shape[1] * scale_factor)
    H = int(image.shape[0] * scale_factor)
    return resize(image, (W, H), interpolation=INTER_LINEAR)


def download(url: str) -> bytes:
    try:
        with urlopen(url) as urlreader:
            response = urlreader.read()
            return response
    except (HTTPError, URLError) as err:
        raise HTTPException(status_code=404, detail=str(err))


def load_cv2_image_from_url(
    url: str,
    resize_pixels: int | None,
    readFlag=IMREAD_COLOR,
) -> ndarray:
    """
    Download an image, convert it to a NumPy array, and then read
    it into OpenCV format. Resize if necessary.
    """

    response = download(url)

    image_array = asarray(bytearray(response), dtype='uint8')
    image = imdecode(image_array, readFlag)

    if resize_pixels:
        image = resize_image(image, resize_pixels)

    return image


def url_to_temppath(url: str) -> str:
    """
    Transform a URL into a temporary file path
    """
    basename = hash_object(url) + extension_from_url(url)
    temppath = join(TEMP_DIR, basename)
    return temppath


def url_to_tempfile(
    url: str,
    resize_pixels: int | None,
) -> str:
    """
    Download an image and save it to a tempfile location. Resize if necessary.
    """

    temppath = url_to_temppath(url)

    if resize_pixels:
        image = load_cv2_image_from_url(url, resize_pixels=resize_pixels)
        imwrite(temppath, image)
    else:
        response = download(url)
        with open(temppath, 'wb') as file:
            file.write(response)

    return temppath


def extension_from_url(url: str) -> str:
    """
    Get an extension from a URL (including those with ?raw=true and such at the end))
    """

    extension = ''

    if '.' in url:
        parts = url.split('.')
        extension = parts[-1]
        for sep in ['?']:
            extension = extension.partition(sep)[0]
        if not extension == '':
            extension = '.' + extension

    return extension
