import os

import logging
from constants import CONFIG_OPTIONS
"""
-splits lines
-stores data as dict with key as config option, value as list of values specified within option
-data is originally a string with ",", so split all ","

Gets all config data in terms of the following options
"""

options = {}


def getConfigData(dirPath):
    """
    reads each line, splits with = and ","
    """
    CONFIG_NAME = "config.ini"

    filePath = os.path.join(dirPath, CONFIG_NAME)

    with open(filePath, "r") as file:
        lines = file.read().splitlines()

    for line in lines:
        option, data = line.split("=")
        if option not in CONFIG_OPTIONS:
            logging.error("Option {0} was not found inside existing config options {1}".format(option, CONFIG_OPTIONS))
            raise SyntaxError

        options[option] = data.split(",")
        logging.debug("config: " + str(options[option]))
