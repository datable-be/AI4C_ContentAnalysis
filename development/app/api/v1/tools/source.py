from os.path import join
from fastapi import HTTPException
from numpy import asarray, ndarray
from pydantic import HttpUrl
from requests import get, RequestException
from cv2 import imdecode, imwrite, resize, IMREAD_COLOR, INTER_LINEAR
from PIL import Image
from io import BytesIO

from api.v1.tools.tools import hash_object
from constants import TEMP_DIR, SETTINGS


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
        response = get(url, timeout=5)
        # Raise an exception if the status code is not 200
        response.raise_for_status()
        return response.content
    except RequestException as err:
        raise HTTPException(status_code=404, detail=str(err))


def load_cv2_image_from_source(
    source: str | bytes,
    resize_pixels: int | None,
    url: bool,
    readFlag=IMREAD_COLOR,
) -> ndarray:
    """
    Read or download an image, convert it to a NumPy array, and then read
    it into OpenCV format. Resize if necessary.
    """

    if isinstance(source, bytes):
        data = source
    else:
        data = read_source(source, url=url)

    if not len(data):
        raise HTTPException(status_code=500, detail='invalid image data')

    if len(data) > SETTINGS['max_image_size']:
        raise HTTPException(
            status_code=500, detail='file size exceeds maximum size'
        )

    image_array = asarray(bytearray(data), dtype='uint8')
    image = imdecode(image_array, readFlag)

    if not hasattr(image, 'resize'):
        raise HTTPException(status_code=500, detail='invalid image format')

    if resize_pixels:
        image = resize_image(image, resize_pixels)

    return image


def source_to_temppath(source: str | HttpUrl, url: bool) -> tuple[str, bytes]:
    """
    Transform a source into a temporary file path.
    Return both the name of the path and the image data.
    """

    extension, data = identify_image_type(source, url=url)
    basename = hash_object(source) + extension
    temppath = join(TEMP_DIR, basename)
    return (temppath, data)


def read_source(source: str | HttpUrl, url: bool) -> bytes:
    """
    Read the bytes from a source (either URL or filepath)
    """
    if url:
        return download(str(source))
    else:
        with open(str(source), 'rb') as file:
            return file.read()


def source_to_tempfile(
    source: str | HttpUrl, resize_pixels: int | None, url: bool
) -> tuple[str, bytes]:
    """
    Download an image and save it to a tempfile location. Resize if necessary.
    Return both image file path and data.
    """

    temppath, data = source_to_temppath(source, url=url)

    if resize_pixels:
        image = load_cv2_image_from_source(
            data, resize_pixels=resize_pixels, url=url
        )
        imwrite(temppath, image)
    else:
        with open(temppath, 'wb') as file:
            file.write(data)

    return (temppath, data)


def identify_image_type(source: str | HttpUrl, url: bool) -> tuple[str, bytes]:
    """
    Identify image type from a source
    (including URLs with ?raw=true at the end or without extension,
     e.g. https://digitalcollections.universiteitleiden.nl/view/item/360453/datastream/JPG/)
    Returns image file extension and data
    """

    data = read_source(source, url=url)

    img = Image.open(BytesIO(data))
    format = img.format

    if not format:
        raise Exception('Cannot determine image format')

    extension = f'.{format.lower()}'

    return (extension, data)
