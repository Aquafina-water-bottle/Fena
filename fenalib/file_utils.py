import os
import errno

def make_dirs(file_path):
    """
    Makes the directories if the directories to the file path does not exist

    Args:
        file_path (str): the path-like object to the file

    Answer comes from:
        https://stackoverflow.com/a/12517490
    """
    dir_path = os.path.realpath(os.path.dirname(file_path))
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except OSError as e: # Guard against race condition
            if e.errno != errno.EEXIST:
                raise


