import os
import logging

FILE_LEVEL = logging.DEBUG
CONSOLE_LEVEL = logging.WARNING

# the logging resets itself so all lines will be updated
FILE_MODE = "w"

# year/month/day with a 24 hour time
FILE_DATE_FMT = "%Y/%m/%d %H:%M:%S"
CONSOLE_DATE_FMT = "%H:%M:%S"

# requires a .format with the file name
FORMAT = "[%(asctime)s] [{}/%(levelname)s]: %(message)s"


def setup_logging(file_path=None):
    """
    creates 2 loggers:
        file logger, set at the debug level
        console logger, set at the warning level
    """

    # note that the file path is relative to this file only no matter where this is imported
    if file_path is None:
        file_path = "log/debug_info.log"
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(dir_path, file_path)

    # make directories if it doesn't exista
    if not os.path.isfile(file_path):
        os.makedirs(os.path.dirname(file_path))

    # actually sets up the logger
    logging.basicConfig(format=FORMAT.format("?"), datefmt=FILE_DATE_FMT, filename=file_path, level=FILE_LEVEL, filemode=FILE_MODE)

    # sets up the console logger
    console = logging.StreamHandler()
    console.setLevel(CONSOLE_LEVEL)
    console_formatter = logging.Formatter(FORMAT.format("?"), datefmt=CONSOLE_DATE_FMT)
    console.setFormatter(console_formatter)
    logging.getLogger().addHandler(console)

    logging.debug("Logger has been set up")


def format_file_name(file_name):
    """
    Simple "hack" to format the logger to include the file name when it didn't before
    """
    log_format = FORMAT.format(file_name)
    file_formatter = logging.Formatter(log_format, datefmt=FILE_DATE_FMT)
    console_formatter = logging.Formatter(log_format, datefmt=CONSOLE_DATE_FMT)

    file_handler, console_handler = logging.getLogger().handlers
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)


# setup_logging()

def test():
    setup_logging()
    logging.debug("test entry")

if __name__ == "__main__":
    test()
