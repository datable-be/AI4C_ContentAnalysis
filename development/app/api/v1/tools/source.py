from os.path import join
from fastapi import HTTPException
from numpy import asarray, ndarray
from requests import get, RequestException
from cv2 import imdecode, imwrite, resize, IMREAD_COLOR, INTER_LINEAR

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
    source: str,
    resize_pixels: int | None,
    url: bool,
    readFlag=IMREAD_COLOR,
) -> ndarray:
    """
    Read or download an image, convert it to a NumPy array, and then read
    it into OpenCV format. Resize if necessary.
    """

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


def source_to_temppath(source: str) -> str:
    """
    Transform a source into a temporary file path
    """
    basename = hash_object(source) + extension_from_source(source)
    temppath = join(TEMP_DIR, basename)
    return temppath


def read_source(source: str, url: bool) -> bytes:
    """
    Read the bytes from a source (either URL or filepath)
    """
    if url:
        return download(source)
    else:
        with open(source, 'rb') as file:
            return file.read()


def source_to_tempfile(
    source: str, resize_pixels: int | None, url: bool
) -> str:
    """
    Download an image and save it to a tempfile location. Resize if necessary.
    """

    temppath = source_to_temppath(source)

    if resize_pixels:
        image = load_cv2_image_from_source(
            source, resize_pixels=resize_pixels, url=url
        )
        imwrite(temppath, image)
    else:
        data = read_source(source, url=url)

        with open(temppath, 'wb') as file:
            file.write(data)

    return temppath


def extension_from_source(source: str) -> str:
    """
    Get an extension from a source (including URLs with ?raw=true and such at the end))
    """

    extension = ''

    if '.' in source:
        parts = source.split('.')
        extension = parts[-1]
        for sep in ['?']:
            extension = extension.partition(sep)[0]
        if not extension == '':
            extension = '.' + extension

    return extension
