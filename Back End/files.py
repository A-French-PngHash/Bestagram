import os


def prepare_directory(dir: str):
    """
    Prepare a directory. Create it if it not already exists.
    :return:
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
