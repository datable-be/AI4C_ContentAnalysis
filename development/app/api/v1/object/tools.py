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
    with urlopen(url) as urlreader:
        response = urlreader.read()
    #  try:
    #      with urlopen(url) as urlreader:
    #          response = urlreader.read()
    #  except (HTTPError, URLError) as err:
    #      print(err)
    #      raise HTTPException(status_code=404, detail=str(err))

    image_array = asarray(bytearray(response), dtype="uint8")
    image = imdecode(image_array, readFlag)

    print(type(image))

    return image
