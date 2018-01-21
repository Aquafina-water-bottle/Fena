"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/lsbasi-part1/
"""

sVersion, vVersion = "s3.0.0", "v2.0.1-ALPHA"

import sys
import logging

from CCU.lexer import Lexer
from CCU.parser import Parser
from CCU.semanticAnalyzer import SemanticAnalyzer
from CCU.interpreter import Interpreter

def main():
    setupLogger()
    text = getFileContents()
    
    lexer = Lexer(text)
    parser = Parser(lexer)
    tree = parser.parse()

    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.visit(tree)
    except Exception as e:
        logging.exception(e)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    logging.debug('Run-time GLOBAL_MEMORY contents:')
    
    # error is that GLOBAL_MEMORY doesn't have anything
    for k, v in sorted(interpreter.GLOBAL_MEMORY.items()):
        logging.debug('%s = %s' % (k, v))

def getFileContents():
    """
    Gets the file contents within the main file

    -if there is no file, uses the default "_text.txt" file
        -if that doesn't exist, default python error lol
    -if there is no contents within the file:
        EOFError
    """
    
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        fileName = "_test.txt"
        logging.warn("'{}' is being used because there were no command line arguments".format(fileName))
        
    with open(fileName, "r") as file:
        text = file.read()
        logging.info("Opening file '{}'".format(fileName))

    if not text:
        logging.error("{} does not contain anything".format(fileName))
        raise EOFError
        
    return text

def setupLogger():
    """
    creates 2 loggers:
        file logger, set at the debug level
        console logger, set at the warning level
    """
    
    fileName = "debug_info.log"
    fileLevel = logging.DEBUG
    consoleLevel = logging.WARNING

    # generally set to "a" (default) unless internal debugging of the logger is required
    # in which case, it is set to "w"
    fileMode = "w"
    
    # year/month/day with a 24 hour time
    fileDateFmt = "%Y/%m/%d %H:%M:%S"
    consoleDateFmt = "%H:%M:%S"
    logFormat = "[%(asctime)s] [%(levelname)s]: %(message)s"
    
    # actually sets up the logger
    logging.basicConfig(format=logFormat, datefmt=fileDateFmt, filename=fileName, level=fileLevel, filemode=fileMode)
    
    # sets up the console logger
    console = logging.StreamHandler()
    console.setLevel(consoleLevel)
    consoleFormatter = logging.Formatter(logFormat, datefmt=consoleDateFmt)
    console.setFormatter(consoleFormatter)
    logging.getLogger().addHandler(console)

if __name__ == '__main__':
    main()