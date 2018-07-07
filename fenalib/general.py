import os
import sys
import argparse

if __name__ == "__main__":
    sys.path.append("..")

# import pyexpander.lib as pyexpander
import fena_pyexpander.lib as pyexpander

from fenalib.pre_pyexpander import parse_pre_pyexpander
from fenalib.lexer import Lexer
from fenalib.parser import Parser
from fenalib.interpreter import Interpreter
from fenalib.writer import Writer, write_after_pre_pyexpander, write_after_pyexpander

semantic_version = "7.0.2"
public_version = "0.4.2-ALPHA"


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
    # parser.add_argument("-dl", "--debug-log", help="outputs the debug log to see all debug info from the Fena language", action="store_true")

    # custom version
    # parser.add_argument("-v", "--version", nargs="?", default=None, help="custom version to override the config file if provided")

    args = parser.parse_args()
    args.output_path = os.path.realpath(args.output_path)
    return args


def parse_text_from_args(text, args, **kwargs):
    return parse_text(text, args.file_name, args.output_path, clean=args.clean, debug=args.debug, **kwargs)


def parse_text(text, file_name, output_path, clean=False, debug=False, use_pre_pyexpander=True, write_functions=True):
    """
    Args:
        file_name (str): File name of the file that will be parsed
            - used for getting the full path to the file and setting the filename for pyexander
        output_path (str): Output path of the mcfunctions
        clean (bool): Whether mcfunctions will be deleted or not
        debug (bool): Whether mcfunctions will be debugged with a say cmd or not
        use_pre_pyexpander (bool): Whether the pre-pyexpander script will be used or not
        write_functions (bool): Whether mcfunctions should be written or not

    Returns:
        list of McFunction objects
    """

    if use_pre_pyexpander:
        text = parse_pre_pyexpander(text)
        write_after_pre_pyexpander(text)

    # add the directory of the file to the import path
    # allows any py commands in the file to import py files relative to said file
    dir_path = os.path.dirname(os.path.realpath(file_name))
    sys.path.append(dir_path)

    # raises an exception if pyexpander fails to parse
    text = pyexpander.expandToStr(text, filename=file_name, auto_indent=True, auto_indent_python=True)[0]
    write_after_pyexpander(text)

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser, output_path)
    mcfunctions = interpreter.interpret()

    if write_functions:
        writer = Writer(mcfunctions, clean, debug)
        writer.write()

    return mcfunctions


