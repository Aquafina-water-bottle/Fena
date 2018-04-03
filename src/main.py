"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/lsbasi-part1/
"""

import subprocess
import logging
import sys
import os

import loggingSetup
from file import writeParsedCmds, writeMcFunctions

# import Mid.lexer
# import Mid.parser
# import Mid.semanticAnalyzer
# import Mid.interpreter

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from configData import getConfigData

sVersion, vVersion = "s6.0.0", "v0.3.0-ALPHA"


def main():
    print("sVersion={}".format(sVersion), "vVersion={}".format(vVersion), sep="\n")

    # required to get relative path of the config, debug_info and parsed_cmds file
    directory = os.path.dirname(__file__)
    
    loggingSetup.setupLogging(directory)
    text, args = file.getContent()
    fileName = args.fileName
    outputPath = args.outputPath

    loggingSetup.formatFileName(fileName)
    configData.getConfigData(directory)

    lexer = Lexer(text, fileName)
    parser = Parser(lexer, outputPath)
    interpreter = Interpreter(parser)
    mcfunctions = Interpreter.interpret(outputPath)
    writeParsedCmds(mcfunctions, directory, args)
    writeMcFunctions(mcfunctions, args)
    # Common.file.writeMacro(mcfunctions, args)

    # lexer = Mid.lexer.Lexer(text, fileName)

    # while not lexer.reachedEOF:
    #     logging.debug(repr(lexer.getNextToken()))

    # print(tokenList)

    # parser = Mid.parser.Parser(lexer)
    # tree = parser.parse()
    #
    # semanticAnalyzer = Mid.semanticAnalyzer.SemanticAnalyzer()
    # semanticAnalyzer.visit(tree)
    #
    # interpreter = Mid.interpreter.Interpreter(tree)
    # result = interpreter.interpret()
    # logging.debug("Run-time GLOBAL_MEMORY contents:")
    #
    # # error is that GLOBAL_MEMORY doesn't have anything
    # for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
    #     logging.debug("%s = %s" % (k, v))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.exception(e)
