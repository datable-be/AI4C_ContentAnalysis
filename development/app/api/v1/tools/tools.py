from hashlib import sha1
from typing import Any


def hash_object(my_object: Any) -> str:
    """
    Create a hash of an object so it can be used as an identifier
    """

    sha_1 = sha1()
    sha_1.update(str(my_object).encode())
    return sha_1.hexdigest()
