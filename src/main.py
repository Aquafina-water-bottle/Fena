"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/lsbasi-part1/
"""

import subprocess
import logging
import sys
import os

import fena.loggingSetup
import fena.file

# import Mid.lexer
# import Mid.parser
# import Mid.semanticAnalyzer
# import Mid.interpreter

import fena.lexer
import fena.parser
import fena.interpreter
import fena.configData

semantic_version = "s6.0.0"
public_version = "v0.3.0-ALPHA"


def main():
    print("Fena:", "semantic_version={}".format(semantic_version), "public_version={}".format(public_version), sep="\n")

    # required to get relative path of the config, debug_info and parsed_cmds file
    directory = os.path.dirname(__file__)
    
    fena.loggingSetup.setupLogging(directory)
    text, args = fena.file.getContent()
    fileName = args.fileName
    outputPath = args.outputPath

    fena.loggingSetup.formatFileName(fileName)
    fena.configData.getConfigData(directory)

    lexer = fena.lexer.Lexer(text, fileName)
    parser = fena.parser.Parser(lexer, outputPath)
    interpreter = fena.interpreter.Interpreter(parser)
    mcfunctions = interpreter.interpret(outputPath)

    fena.file.writeParsedCmds(mcfunctions, directory, args)
    fena.file.writeMcFunctions(mcfunctions, args)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
