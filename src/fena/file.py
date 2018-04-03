import pyexpander.lib as pyexpander
import subprocess
import argparse
import logging
import sys
import os


def getArgs():
    # Usage: main.py fileName [outputPath] [-d, --debug] [-c, --clean]
    parser = argparse.ArgumentParser()

    # requires input file
    parser.add_argument("fileName", help="main ccu file")

    # optional output directory
    defaultOutputPath = "functions/ccu"
    parser.add_argument("outputPath", nargs="?", default=defaultOutputPath, help="the directory in which all mcfunctions will be created, with the default being 'functions/ccu'")

    # cleans mcfunctions
    parser.add_argument("-c", "--clean", help="removes all mcfunction files inside the output directory", action="store_true")

    # debug
    parser.add_argument("-d", "--debug", help="puts say commands at the front of each mcfunction", action="store_true")

    args = parser.parse_args()
    args.outputPath = os.path.abspath(args.outputPath)

    return args


def getContent():
    """
    Gets the file contents within the main file

    -if there is no file, uses the default "_text.txt" file
        -if that doesn't exist, default python error lol
    -if there is no contents within the file:
        EOFError
    """

    args = getArgs()
    fileName = args.fileName

    # gets the file path of the main ccu file
    with open(fileName, "r") as file:
        dirPath = os.path.dirname(os.path.realpath(file.name))

        # add the directory of the file to the import path
        # allows any py commands in the file to import py files relative to said file
        sys.path.append(dirPath)

        # automagically raises an exception if pyexpander fails to parse
        source_file_text = file.read()
        text = pyexpander.expandToStr(source_file_text, filename=fileName)[0]
        logging.debug("\n" + text)

    # print(dirPath, fileName)
    # print("BEFORE {}".format(sys.path))
    # sys.path.append(os.getcwd())
    # print("AFTER {}".format(sys.path))

    # logging.info("Calling pyexpander")
    # expander3path = "expander3.py"
    # process = subprocess.Popen([expander3path, '-i', fileName], stdout=subprocess.PIPE, cwd=dirPath)
    # text, error = process.communicate()
    # text = text.decode("utf-8")
    # logging.debug(text)
    # logging.debug("")
    # logging.debug(error)
    # logging.debug("")

    # with open(fileName, "r") as file:
    #     text = file.read()
    #     logging.info("Opening file '{}'".format(fileName))
    
    return text, args


def addDebugInfo(text, mcfunction, display):
    if display:
        return "    say running {}\n".format(mcfunction.funcPath) + text
    return "say running {}\n".format(mcfunction.funcPath) + text


def cleanOutput(outputPath):
    """
    cleans out all mcfunctions from the output directory
    """

    # gets all files inside the output path
    for file in os.listdir(outputPath):
        filePath = os.path.join(outputPath, file)
        try:
            if os.path.isfile(filePath) and filePath.endswith(".mcfunction"):
                # print("found", filePath)
                os.remove(filePath)
        except Exception as e:
            logging.error(e)


def writeMacro(mcfunctions, args):
    if args.macro is not None:
        with open(args.macro, "w") as file:
            for mcfunction in mcfunctions:
                file.write("$edit_{}".format(mcfunction.name) + "\n")
                file.write("$endmacro" + "\n")
                file.write("$edit_type_{}".format(mcfunction.name) + "\n")
                file.write("$endmacro" + "\n")


def writeParsedCmds(mcfunctions, directory, args):
    FILE_NAME = "parsed_cmds.txt"
    debug = args.debug

    fullPath = os.path.join(directory, FILE_NAME)
    with open(fullPath, "w") as file:
        for mcfunction in mcfunctions:
            function_name = mcfunction.path
            commands = "\n".join("    " + cmd_str for cmd_str in mcfunction.cmd_strs)

            if debug:
                commands = addDebugInfo(commands, mcfunction, True)

            full_function = function_name + "\n" + commands + "\n"

            file.write(full_function + "\n")
            logging.debug(full_function)


def writeMcFunctions(mcfunctions, args):
    outputPath = args.outputPath
    clean = args.clean
    debug = args.debug

    if clean:
        cleanOutput(outputPath)
        
    for mcfunction in mcfunctions:
        path = os.path.join(outputPath, mcfunction.path)
    
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            commands = "\n".join(mcfunction.cmd_strs)
            if debug:
                commands = addDebugInfo(commands, mcfunction, False)

            file.write(commands + "\n")


