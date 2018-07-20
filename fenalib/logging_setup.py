import os
import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")

from fenalib.file_utils import make_dirs

FILE_LEVEL = logging.DEBUG
CONSOLE_LEVEL = logging.WARNING

# the logging resets itself so all lines will be updated
FILE_MODE = "w"

# year/month/day with a 24 hour time
FILE_DATE_FMT = "%Y/%m/%d %H:%M:%S"
CONSOLE_DATE_FMT = "%H:%M:%S"

# requires a .format with the file name
FORMAT = "[%(asctime)s] [{}/%(levelname)s]: %(message)s"

logger = logging.getLogger()


def setup_logging(debug_file_path="log/debug_info.log"):
    """
    This creates two loggers: file logger (debug), console logger (warning)

    Args:
        debug_file_path (Optional[str]): The file path to the debug info file
            If this is set to None, then this will NOT make a debug info file.
            Otherwise, if left out, the default goes to log/debug_info.log
    """

    # note that the file path is relative to this file only no matter where this is imported/ran
    if debug_file_path is not None:
        dir_path = os.path.dirname(__file__)
        debug_file_path = os.path.join(dir_path, debug_file_path)

        # makes directories if they don't exist
        make_dirs(debug_file_path)

    # sets the log format for both the console and the file format
    log_format = FORMAT.format("<NO FILE>")

    # sets up the console handler
    # if there is already one, that means something like
    # `logging.debug` has been used and set a default handler
    if len(logger.handlers) == 1:
        console_handler = logger.handlers[0]
        logger.handlers.clear()
    else:
        console_handler = logging.StreamHandler()
    logger.handlers.clear()
    console_handler.setLevel(CONSOLE_LEVEL)

    # sets the console formatter
    console_formatter = logging.Formatter(log_format, datefmt=CONSOLE_DATE_FMT)
    console_handler.setFormatter(console_formatter)

    if debug_file_path is not None:
        # sets up the default logger before the console formatter because the
        # default logger cannot be set up with a non-empty logging.handlers list
        logging.basicConfig(format=log_format, datefmt=FILE_DATE_FMT, filename=debug_file_path, level=FILE_LEVEL, filemode=FILE_MODE)

    # sets up the console handler
    logger.addHandler(console_handler)

    logging.debug("Logger has been set up")


def format_file_name(file_name):
    """
    Simple "hack" to format the logger to include the file name when it didn't before
    """

    # gets the log format as a string to be used for both the file and console formatter
    log_format = FORMAT.format(file_name)

    # gets the actual formatter objects
    file_formatter = logging.Formatter(log_format, datefmt=FILE_DATE_FMT)
    console_formatter = logging.Formatter(log_format, datefmt=CONSOLE_DATE_FMT)
    formatters = (console_formatter, file_formatter)

    # gets the handlers although the file handler might not exist
    # note that logger.handlers is reversed to ensure the first is the console formatter
    # this is because the file formatter might not exist
    for handler, formatter in zip(reversed(logger.handlers), formatters):
        handler.setFormatter(formatter)


def test():
    logging.warning("test entry")
    setup_logging()
    logging.warning("test entry 2")


if __name__ == "__main__":
    test()

