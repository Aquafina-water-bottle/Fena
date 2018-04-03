import os
import logging

FILE_NAME = "debug_info.log"
FILE_LEVEL = logging.DEBUG
CONSOLE_LEVEL = logging.WARNING

# generally set to "a" (default) unless internal debugging of the logger is required
# in which case, it is set to "w"
FILE_MODE = "w"

# year/month/day with a 24 hour time
FILE_DATE_FMT = "%Y/%m/%d %H:%M:%S"
CONSOLE_DATE_FMT = "%H:%M:%S"
FORMAT = "[%(asctime)s] [{}/%(levelname)s]: %(message)s"


def setupLogging(dirPath):
    """ creates 2 loggers:
        file logger, set at the debug level
        console logger, set at the warning level
    """

    filePath = os.path.join(dirPath, FILE_NAME)
    
    # actually sets up the logger
    logging.basicConfig(format=FORMAT.format("?"), datefmt=FILE_DATE_FMT, filename=filePath, level=FILE_LEVEL, filemode=FILE_MODE)
    
    # sets up the console logger
    console = logging.StreamHandler()
    console.setLevel(CONSOLE_LEVEL)
    consoleFormatter = logging.Formatter(FORMAT.format("?"), datefmt=CONSOLE_DATE_FMT)
    console.setFormatter(consoleFormatter)
    logging.getLogger().addHandler(console)

    
def formatFileName(fileName):
    """
    simple "hack" to format the logger to include the file name when it didn't before
        -once imports are a thing, this probably has to be changed
    """
    logFormat = FORMAT.format(fileName)
    fileFormatter = logging.Formatter(logFormat, datefmt=FILE_DATE_FMT)
    consoleFormatter = logging.Formatter(logFormat, datefmt=CONSOLE_DATE_FMT)
    
    fileHandler, consoleHandler = logging.getLogger().handlers
    fileHandler.setFormatter(fileFormatter)
    consoleHandler.setFormatter(consoleFormatter)
