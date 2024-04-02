from hashlib import sha1
from typing import Any
from fastapi.responses import HTMLResponse
from pathlib import Path

from classes import (
    ObjectRequest,
    ColorRequest,
)

from constants import IMAGE_DIR


def hash_object(my_object: Any) -> str:
    """
    Create a hash of an object so it can be used as an identifier
    """

    sha_1 = sha1()
    sha_1.update(str(my_object).encode())
    return sha_1.hexdigest()


def ui_template(ui_file: str) -> HTMLResponse:
    """
    Fill a HTML template file for user interface
    """

    localfiles = ''
    for path in Path(IMAGE_DIR).iterdir():
        localfiles += f'<option>{str(path.name)}</option>'

    with open(ui_file, 'r') as reader:
        content = reader.read()
        if localfiles:
            placeholder = '<option></option>'
            content = content.replace(placeholder, placeholder + localfiles)
        return HTMLResponse(content=content)
