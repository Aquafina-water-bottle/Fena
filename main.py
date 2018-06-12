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

import fena.logging_setup
import fena.lexer
import fena.parser
import fena.writer
import fena.interpreter

semantic_version = "s6.0.0"
public_version = "v0.3.0-ALPHA"

def get_args():
    # Usage: main.py fileName [output_path] [-d, --debug] [-c, --clean]
    parser = argparse.ArgumentParser()

    # requires input file
    parser.add_argument("file_name", help="main ccu file")

    # optional output directory
    defaultOutputPath = "functions/ccu"
    parser.add_argument("output_path", nargs="?", default=defaultOutputPath, help="the directory in which all mcfunctions will be created, with the default being 'functions/ccu'")

    # cleans mcfunctions
    parser.add_argument("-c", "--clean", help="removes all mcfunction files inside the output directory", action="store_true")

    # debug
    parser.add_argument("-d", "--debug", help="puts say commands at the front of each mcfunction", action="store_true")

    # debug log
    parser.add_argument("-dl", "--debug-log", help="outputs the debug log to see all debug info from the Fena language", action="store_true")

    args = parser.parse_args()
    args.output_path = os.path.abspath(args.output_path)
    return args


def get_content(args):
    """
    Gets the file contents within the main file

    Raises:
        EOFError: if there is literally no content on the main file
    """

    file_name = args.file_name

    # gets the file path of the main ccu file
    with open(file_name, "r") as file:
        dir_path = os.path.dirname(os.path.realpath(file.name))

        # add the directory of the file to the import path
        # allows any py commands in the file to import py files relative to said file
        sys.path.append(dir_path)
        source_file_text = file.read()

        # raises an exception if pyexpander fails to parse
        text = pyexpander.expandToStr(source_file_text, filename=file_name)[0]
        logging.debug("\n" + text)

    return text


def main():
    print("Fena:", "semantic_version={}".format(semantic_version), "public_version={}".format(public_version), sep="\n")

    args = get_args()

    # required to get relative path of the config, debug_info and parsed_cmds file
    text = get_content(args)
    file_name = args.file_name
    output_path = args.output_path

    # sets the file name for logging
    fena.logging_setup.format_file_name(file_name)

    lexer = fena.lexer.Lexer(text)
    parser = fena.parser.Parser(lexer)
    interpreter = fena.interpreter.Interpreter(parser, output_path)
    mcfunctions = interpreter.interpret()

    writer = fena.writer.Writer(mcfunctions, args.clean, args.debug)
    writer.write()

if __name__ == '__main__':
    # try:
    #     main()
    # except Exception as e:
    #     logging.exception(e)
    get_args()
