"""
A butt load of code shameless taken from Ruslan Spivak's tutorial for making an interpreter:
    https://ruslanspivak.com/lsbasi-part1/

blocks.txt and entities.txt shamelessly taken from:
    https://github.com/PepijnMC/Minecraft
"""

import argparse
import logging
import sys
import os

import pyexpander.lib as pyexpander

import fenalib.logging_setup as logging_setup
logging_setup.setup_logging()
from fenalib.config_data import get_all_data
from fenalib.pre_pyexpander import parse_pre_pyexpander
from fenalib.lexer import Lexer
from fenalib.parser import Parser
from fenalib.interpreter import Interpreter
from fenalib.writer import Writer, write_after_pre_pyexpander, write_after_pyexpander

semantic_version = "s6.0.0"
public_version = "v0.3.0-ALPHA"

def get_args():
    # Usage: main.py fileName [output_path] [-d, --debug] [-c, --clean]
    parser = argparse.ArgumentParser()

    # requires input file
    parser.add_argument("file_name", help="main fena file")

    # optional output directory
    default_output_path = "functions/fena"
    parser.add_argument("output_path", nargs="?", default=default_output_path,
                        help="the directory in which all mcfunctions will be created, with the default being 'functions/fena'")

    # cleans mcfunctions
    parser.add_argument("-c", "--clean", help="removes all mcfunction files inside the output directory", action="store_true")

    # debug
    parser.add_argument("-d", "--debug", help="puts say commands at the front of each mcfunction to show who is running it", action="store_true")

    # debug log
    parser.add_argument("-dl", "--debug-log", help="outputs the debug log to see all debug info from the Fena language", action="store_true")

    # custom version
    parser.add_argument("-v", "--version", nargs="?", default=None, help="custom version to override the config file if provided")

    args = parser.parse_args()
    args.output_path = os.path.realpath(args.output_path)
    return args


def main():
    print(f"Fena: semantic_version={semantic_version}, public_version={public_version}")

    # checks for python version (must be greater than or equal to 3.6)
    if not (sys.version_info.major >= 3 and sys.version_info.minor >= 6):
        raise RuntimeError("Python version must be 3.6")

    # gets all command line arguments
    args = get_args()

    #  overrides the version if necessary
    if args.version is not None:
        get_all_data(args.version)

    file_name = args.file_name
    output_path = args.output_path
    with open(file_name) as file:
        text = file.read()

    # pre pyexpander
    text = parse_pre_pyexpander(text)
    write_after_pre_pyexpander(text)

    # add the directory of the file to the import path
    # allows any py commands in the file to import py files relative to said file
    dir_path = os.path.dirname(os.path.realpath(file_name))
    sys.path.append(dir_path)

    # raises an exception if pyexpander fails to parse
    text = pyexpander.expandToStr(text, filename=file_name)[0]
    write_after_pyexpander(text)

    # sets the file name for logging
    logging_setup.format_file_name(file_name)

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser, output_path)
    mcfunctions = interpreter.interpret()

    writer = Writer(mcfunctions, args.clean, args.debug)
    writer.write()

if __name__ == '__main__':
    # print("test")

    try:
        main()
    except Exception as e:
        logging.exception(e) # type: ignore

