from pathlib import Path
from time import time


def housekeeping(directory: str) -> None:
    """
    Empty a directory of files older than one day
    """

    directory_path = Path(directory)

    check_file = directory_path / '.housekeeping'

    # Create check_file if it does not exist
    if not check_file.exists():
        check_file.touch()

    now = time()

    # Return if check_file is younger than one day
    if check_file.stat().st_mtime > now - 24 * 60 * 60:
        return None

    for filepath in directory_path.iterdir():
        if str(filepath.name) == '.housekeeping':
            continue

        # Remove if the file is older than one day
        if filepath.stat().st_mtime < now - 24 * 60 * 60:
            filepath.unlink()
            print(f'housekeeping: {filepath} removed')

    # Update checkfile
    check_file.touch()
