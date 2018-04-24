"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/lsbasi-part1/
"""

import argparse
import logging
import sys
import os

import fena.logging_setup
import fena.file
import fena.lexer
import fena.parser
import fena.writer
# import fena.interpreter

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

    args = parser.parse_args()
    args.output_path = os.path.abspath(args.output_path)

    return args


def main():
    print("Fena:", "semantic_version={}".format(semantic_version), "public_version={}".format(public_version), sep="\n")

    args = get_args()

    # required to get relative path of the config, debug_info and parsed_cmds file
    text = fena.file.get_content(args)
    file_name = args.file_name
    output_path = args.output_path

    # sets the file name for logging
    fena.logging_setup.format_file_name(file_name)

    lexer = fena.lexer.Lexer(text)
    parser = fena.parser.Parser(lexer, output_path)
    parser.parse()

    writer = fena.writer.Writer(parser.mcfunctions, args)
    writer.write()

    # interpreter = fena.interpreter.Interpreter(parser)
    # mcfunctions = interpreter.interpret(output_path)

    # fena.file.write_parsed_cmds(mcfunctions, args)
    # fena.file.write_mc_functions(mcfunctions, args)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
