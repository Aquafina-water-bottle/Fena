#!/usr/bin/env python3

"""
Fena simple
- Uses pre-pyexpander
"""

import logging
import fenalib.logging_setup as logging_setup
logging_setup.setup_logging()

from fenalib.general import main


if __name__ == '__main__':
    # print("test")

    try:
        main()
    # pylint: disable=broad-except
    except Exception as e:
        logging.exception(e) # type: ignore

