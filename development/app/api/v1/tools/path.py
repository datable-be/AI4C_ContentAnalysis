import os
from pathlib import Path
import time


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
