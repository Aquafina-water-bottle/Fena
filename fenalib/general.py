import os
import sys
import argparse

if __name__ == "__main__":
    sys.path.append("..")

# import pyexpander.lib as pyexpander
import fena_pyexpander.lib as pyexpander

from fenalib.pre_pyexpander import parse_pre_pyexpander
from fenalib.writer import Writer, write_after_pre_pyexpander, write_after_pyexpander
from fenalib.config_data import PreConfigData


__all__ = [
    "SEMANTIC_VERSION",
    "PUBLIC_VERSION",
    "VersionedData",
    "check_py_version",
    "get_args",
    "parse_text",
    "main",
    ]

SEMANTIC_VERSION = "7.0.3"
PUBLIC_VERSION = "0.4.2-ALPHA"


class VersionedData:
    def __init__(self, version):
        pass


def check_py_version():
    # checks for python version (must be greater than or equal to 3.6)
    if not (sys.version_info.major >= 3 and sys.version_info.minor >= 6):
        raise RuntimeError("Python version must be 3.6 or greater")


def get_args():
    # Usage: main.py fileName [output_path] [-d, --debug] [-c, --clean]
    parser = argparse.ArgumentParser()

    # requires input file
    parser.add_argument("file_name", help="main fena file")

    # optional output directory
    default_output_path = "functions/fena"
    parser.add_argument("output_path", nargs="?", default=default_output_path,
                        help="the directory in which all mcfunctions will be created, with the default being 'functions/fena'")

    parser.add_argument("-v", "--version", help="Sets the minecraft version", action="TODO")
    # parser.add_argument("-v", "--version", nargs="?", default=None, help="custom version to override the config file if provided")
    parser.add_argument("-s", "--simple", help="parse commands without shortcuts", action="store_true")
    parser.add_argument("-c", "--clean", help="removes all mcfunction files inside the output directory", action="store_true")
    parser.add_argument("-d", "--debug", help="puts say commands at the front of each mcfunction to show who is running it", action="store_true")
    parser.add_argument("-e", "--ego", help="outputs the debug log to see all debug info from the Fena language", action="store_true")
    parser.add_argument("-l", "--debug-log", help="outputs the debug log to see all debug info from the Fena language", action="store_true")

    # custom version

    args = parser.parse_args()
    args.output_path = os.path.realpath(args.output_path)
    return args


# def parse_text_from_args(text, args, **kwargs):
#     return parse_text(text, args.file_name, args.output_path, clean=args.clean, debug=args.debug, **kwargs)


def parse_text(text, use_pre_pyexpander=True, write_functions=True):
    """
    Args:
        use_pre_pyexpander (bool): Whether the pre-pyexpander script will be used or not
        write_functions (bool): Whether mcfunctions should be written or not

    Returns:
        list of McFunction objects
    """

    if use_pre_pyexpander:
        text = parse_pre_pyexpander(text)
        write_after_pre_pyexpander(text)

    pre_config_data = PreConfigData()

    # add the directory of the file to the import path
    # allows any py commands in the file to import py files relative to said file
    dir_path = os.path.dirname(os.path.realpath(file_name))
    sys.path.append(dir_path)

    # raises an exception if pyexpander fails to parse
    text = pyexpander.expandToStr(text, filename=file_name, auto_indent=True, auto_indent_python=True)[0]
    write_after_pyexpander(text)

    versioned_data = VersionedData(pre_config_data.version)

    lexer = versioned_data.Lexer(text)
    parser = versioned_data.Parser(lexer)
    interpreter = versioned_data.Interpreter(parser)
    mcfunctions = interpreter.interpret()

    if write_functions:
        writer = versioned_data.Writer(mcfunctions, clean, debug)
        writer.write()

    return mcfunctions


def main():
    check_py_version()

    print(f"Fena: semantic_version={semantic_version}, public_version={public_version}")

    # gets all command line arguments
    args = get_args()

    #  overrides the version if necessary
    # if args.version is not None:
    #     get_all_data(args.version)

    with open(args.file_name) as file:
        text = file.read()

    config_dict = get_config_dict()
    get_pre_config(text, args, config_dict)

    # sets the file name for logging
    logging_setup.format_file_name(args.file_name)

    parse_text(text)
    # parse_text_from_args(text, args)


