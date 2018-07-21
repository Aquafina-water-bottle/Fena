#!/usr/bin/env python3

"""
`python3 -m unittest discover -s unittests`
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

