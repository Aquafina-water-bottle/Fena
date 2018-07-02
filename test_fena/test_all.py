"""
The main testing module for fena
Note that this is named "test_fena" because the "test" module is already taken
"""

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

import logging
import time

import fenalib.logging_setup as logging_setup
logging_setup.setup_logging()

from fenalib.config_data import get_all_data, ConfigData
from fenalib.in_file_config import InFileConfig

import test_fena.v1_12.test_all
# import test_fena.v1_13.test_all
import test_fena.other.test_all
import test_fena.test_common

logging_setup.format_file_name("test_cases")

# simply finalizes the in file config so the command builder can work and defaults can be used
in_file_config = InFileConfig()
in_file_config.finalize()

config_data = ConfigData()

begin = time.perf_counter()

try:
    logging.debug("\n\nother")
    test_fena.other.test_all.test_all()

    logging.debug("\n\n1.12")
    get_all_data("1.12")
    # sets ego to false to remove unnecessary warnings
    config_data.ego = False
    test_fena.v1_12.test_all.test_all()

    # logging.debug("\n\n1.13")
    # get_all_data("1.13")
    # config_data.ego = False
    # test_fena.v1_13.test_all.test_all()

except Exception as e:  # pylint: disable=broad-except
    # ignores the mypy warning idk
    logging.exception(e)  # type: ignore

else:
    end = time.perf_counter()
    logging.warning(f"Test cases finished in {end-begin} seconds")


