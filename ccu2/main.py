"""
Shoutout to Ruslan Spivak for pretty much providing the bedrock code to this interpreter
    His tutorial for making an interpreter can be found here: https://ruslanspivak.com/ 

How versioning works:
    s#_#_# refers to the semantic version, which comes with their strict rules
        -this will be used for internal reference since it provides better info for the programmer compared to the public version
    v#_#_# refers to the public version, which is mostly me intrementing the major / minor / patch whenever I feel necessary
        -eg. if this program makes backwards incompatable changes that affects 0.001% of the users,
         I'll update the major in the semantic version, but I'll update either the minor or patch in the public version
         
s2.0.0:
    Mostly reorganizing a huge chunk of the pascal interpreter
        -Got a logger working
        -Things are in modules now
"""

import sys
import logging

from s2_0_0.lexer import Lexer
from s2_0_0.parser import Parser
from s2_0_0.semanticAnalyzer import SemanticAnalyzer
from s2_0_0.interpreter import Interpreter

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
        logging.debug(e)

    interpreter = Interpreter(tree)
    result = interpreter.interpret()
    logging.debug('')
    logging.debug('Run-time GLOBAL_MEMORY contents:')
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