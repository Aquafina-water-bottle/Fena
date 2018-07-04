#!/usr/bin/env python3

"""
A butt load of code shamelessly taken from Ruslan Spivak's tutorial for making an interpreter:
    https://ruslanspivak.com/lsbasi-part1/

Pyexpander code shamelessly taken from:
    http://pyexpander.sourceforge.net/

Lots of config files shamelessly gotten from:
    https://github.com/PepijnMC/Minecraft
    https://github.com/Arcensoth/mcdata
"""

"""
Random stuff only for me honestly (vim session tab numbers):
    1: Python3/fena
        fena.py
    2: Fena/lib
        floo_event.py
        location.py
    3: floo_network/src
        main.py
        main.fena
    4: Python3/fena/fenalib/log
        after_pre_pyexpander.txt
        after_pyexpander.txt
        parsed_cmds.txt
    5: Fena.wiki
        Code-Style.md
        Code-Documentation.md
"""

import logging
import sys

import fenalib.logging_setup as logging_setup
logging_setup.setup_logging()

from fenalib.general import parse_text_from_args, get_args, semantic_version, public_version
# from fenalib.config_data import get_all_data


def main():
    # checks for python version (must be greater than or equal to 3.6)
    if not (sys.version_info.major >= 3 and sys.version_info.minor >= 6):
        raise RuntimeError("Python version must be 3.6 or greater")

    print(f"Fena: semantic_version={semantic_version}, public_version={public_version}")

    # gets all command line arguments
    args = get_args()

    #  overrides the version if necessary
    # if args.version is not None:
    #     get_all_data(args.version)

    with open(args.file_name) as file:
        text = file.read()

    # sets the file name for logging
    logging_setup.format_file_name(args.file_name)
    # parse_text(text, file_name, output_path, clean=args.clean, debug=args.debug)
    parse_text_from_args(text, args)


if __name__ == '__main__':
    # print("test")

    try:
        main()
    # pylint: disable=broad-except
    except Exception as e:
        logging.exception(e) # type: ignore

