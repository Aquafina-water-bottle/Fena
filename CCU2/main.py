"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/lsbasi-part1/
"""

import subprocess
import logging
import sys
import os

import Common.loggingSetup
import Common.file

# import Mid.lexer
# import Mid.parser
# import Mid.semanticAnalyzer
# import Mid.interpreter

import Post.lexer
import Post.parser
import Post.interpreter
import Post.configData

sVersion, vVersion = "s5.1.1", "v0.2.1-ALPHA"


def main():
    print("sVersion={}".format(sVersion), "vVersion={}".format(vVersion), sep="\n")

    # required to get relative path of the config, debug_info and parsed_cmds file
    directory = os.path.dirname(__file__)
    
    Common.loggingSetup.setupLogging(directory)
    text, args = Common.file.getContent()
    fileName = args.fileName
    outputPath = args.outputPath

    Common.loggingSetup.formatFileName(fileName)
    Post.configData.getConfigData(directory)

    lexer = Post.lexer.Lexer(text, fileName)
    parser = Post.parser.Parser(lexer, outputPath)
    interpreter = Post.interpreter.Interpreter(parser)
    mcfunctions = interpreter.interpret(outputPath)
    Common.file.writeParsedCmds(mcfunctions, directory, args)
    Common.file.writeMcFunctions(mcfunctions, args)

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
