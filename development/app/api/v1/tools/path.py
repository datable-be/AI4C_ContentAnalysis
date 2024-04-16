from pathlib import Path
from time import time

from constants import SETTINGS


def housekeeping(directory: str) -> None:
    """
    Empty a directory of files older than the configuration
    defined in the application settings
    """

    directory_path = Path(directory)

    check_file = directory_path / '.housekeeping'

    # Create check_file if it does not exist
    if not check_file.exists():
        check_file.touch()

    now = time()

    # Return if check_file is younger than one day
    if check_file.stat().st_mtime > now - SETTINGS['housekeeping_interval']:
        return None

    for filepath in directory_path.iterdir():
        if str(filepath.name) == '.housekeeping':
            continue

        # Remove if the file is older than one day
        if filepath.stat().st_mtime < now - SETTINGS['housekeeping_interval']:
            filepath.unlink()
            print(f'housekeeping: {filepath} removed')

    # Update checkfile
    check_file.touch()
