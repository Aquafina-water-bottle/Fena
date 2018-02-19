import pyexpander.lib as pyexpander
import subprocess
import logging
import sys
import os

DEFAULT_FILE = "_post_test.txt"


def getContent():
    """
    Gets the file contents within the main file

    -if there is no file, uses the default "_text.txt" file
        -if that doesn't exist, default python error lol
    -if there is no contents within the file:
        EOFError
    """

    fileName = DEFAULT_FILE
    outputPath = os.path.abspath("output")
    for index in range(len(sys.argv)):
        argument = sys.argv[index]
        if index == 1:
            fileName = argument
        if index == 2:
            outputPath = os.path.abspath(argument)
            # outputPath = argument

    if fileName == DEFAULT_FILE:
        logging.warning("'{}' is being used because there were no command line arguments".format(fileName))

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
    
    return text, fileName, outputPath


def writeParsedCmds(directory, mcfunctions):
    FILE_NAME = "parsed_cmds.txt"
    fullPath = os.path.join(directory, FILE_NAME)
    with open(fullPath, "w") as file:
        for mcfunction in mcfunctions:
            function_name = mcfunction.path
            commands = "\n".join("    " + cmd_str for cmd_str in mcfunction.cmd_strs)
            full_function = function_name + "\n" + commands + "\n"

            file.write(full_function + "\n")
            logging.debug(full_function)


def writeMcFunctions(outputPath, mcfunctions):
    for mcfunction in mcfunctions:
        path = os.path.join(outputPath, mcfunction.path)
    
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            commands = "\n".join(mcfunction.cmd_strs)
            file.write(commands + "\n")


