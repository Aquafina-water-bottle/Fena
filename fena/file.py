import pyexpander.lib as pyexpander
import argparse
import logging
import sys
import os


def get_content(args):
    """
    Gets the file contents within the main file

    -if there is no contents within the file:
        EOFError
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


def write_parsed_cmds(mcfunctions, args):
    FILE_NAME = "parsed_cmds.txt"
    debug = args.debug
    dir_path = os.path.dirname(__file__)

    full_path = os.path.join(dir_path, FILE_NAME)

    with open(full_path, "w") as file:
        for mcfunction in mcfunctions:
            function_name = mcfunction.path
            commands = "\n".join("    " + cmd_str for cmd_str in mcfunction.cmd_strs)

            if debug:
                commands = add_debug_info(commands, mcfunction, True)

            full_function = function_name + "\n" + commands + "\n"

            file.write(full_function + "\n")
            logging.debug(full_function)


def write_mc_functions(mcfunctions, args):
    output_path = args.output_path
    clean = args.clean
    debug = args.debug

    if clean:
        clean_output(output_path)
        
    for mcfunction in mcfunctions:
        path = os.path.join(output_path, mcfunction.path)
    
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as file:
            commands = "\n".join(mcfunction.cmd_strs)
            if debug:
                commands = add_debug_info(commands, mcfunction, False)

            file.write(commands + "\n")


def add_debug_info(text, mcfunction, display):
    """
    TODO:
        Change the actual mcfunction instead of the files
    """
    if display:
        return "    say running {}\n".format(mcfunction.funcPath) + text
    return "say running {}\n".format(mcfunction.funcPath) + text


def clean_output(output_path):
    """
    Cleans out all mcfunctions from the output directory

    TODO:
        Change to have the folders be recorded and also removed
    """

    # gets all files inside the output path
    for file in os.listdir(output_path):
        filePath = os.path.join(output_path, file)

        # the following might raise an error
        if os.path.isfile(filePath) and filePath.endswith(".mcfunction"):
            # print("found", filePath)
            os.remove(filePath)
