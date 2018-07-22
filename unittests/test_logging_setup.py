import unittest
import logging
import os

from io import StringIO

import fenalib.logging_setup as logging_setup

class TestLoggingSetup(unittest.TestCase):
    def test_setup_control(self):
        string_io = StringIO()
        logging.basicConfig(stream=string_io)
        logging_setup.setup_logging()
        logging.warning("test after setup logging")

        print()
        logging_setup.format_file_name("_test_logging_setup.py")
        logging.warning("test after file name setup")

        print()
        logging.warning("test final")


        pass

    def test_setup(self):
        pass

"""
import logging
import os

if __name__ == "__main__":
    import sys
    sys.path.append("..")

import fenalib.logging_setup as logging_setup


def import_test():
    logging.warning("test initial")

    print()
    # logging_setup.setup_logging(debug_file_path=None)
    logging_setup.setup_logging()
    logging.warning("test after setup logging")
    logging.warning(f"handlers: {logging.getLogger().handlers}")

    print()
    logging_setup.format_file_name("_test_logging_setup.py")
    logging.warning("test after file name setup")

    print()
    logging.warning("test final")


def test():
    logging.warning("test initial")

    FILE_LEVEL = logging.DEBUG

    # the logging resets itself so all lines will be updated
    FILE_MODE = "w"

    # year/month/day with a 24 hour time
    FILE_DATE_FMT = "%Y/%m/%d %H:%M:%S"

    # requires a .format with the file name
    FORMAT = "[%(asctime)s] [{}/%(levelname)s]: %(message)s"

    # gets file path
    file_path = "log/debug_info.log"
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, file_path)

    logging.basicConfig(format=FORMAT.format("?"), datefmt=FILE_DATE_FMT, filename=file_path, level=FILE_LEVEL, filemode=FILE_MODE)

    logging.warning("test final")


if __name__ == "__main__":
    import_test()

"""
