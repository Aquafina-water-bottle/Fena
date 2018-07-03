import os
import logging

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.mcfunction import McFunction
from fenalib.assert_utils import assert_type, assert_list_types

PATH_TO_LOG_DIR = "log"

def write_after_pre_pyexpander(text):
    current_dir_path = os.path.dirname(__file__)
    after_pre_pyexpander_path = os.path.join(current_dir_path, PATH_TO_LOG_DIR, "after_pre_pyexpander.txt")
    with open(after_pre_pyexpander_path, "w") as file:
        file.write(text)
    logging.debug("Successfully wriitten 'after_pre_pyexpander.txt'")


def write_after_pyexpander(text):
    current_dir_path = os.path.dirname(__file__)
    after_pyexpander_path = os.path.join(current_dir_path, PATH_TO_LOG_DIR, "after_pyexpander.txt")
    with open(after_pyexpander_path, "w") as file:
        file.write(text)
    logging.debug("Successfully wriitten 'after_pyexpander.txt'")


class Writer:
    """
    Literally writes out all the proper files

    Attributes:
        mcfunctions (list or tuple of McFunction objects)
        clean (bool): Whether the mcfunctions should be deleted or not
        debug (bool): Whether a debug command should be added to all commands or not

    Writes:
        - each mcfunction file based off of their full path
        - fenalib/log/parsed_cmds.txt to summarize all commands for each mcfunction file
    """

    def __init__(self, mcfunctions, clean=False, debug=False):
        assert_list_types(mcfunctions, McFunction)
        assert_type(clean, bool)
        assert_type(debug, bool)
        self.mcfunctions = tuple(mcfunctions)
        self.clean = clean
        self.debug = debug

    def _get_mcfunction_paths(self):
        """
        Returns:
            set of str objects: All possible paths for the mcfunctions to clean
        """
        return {os.path.dirname(mcfunction.full_path) for mcfunction in self.mcfunctions}

    def clean_files(self):
        """
        All files ending with .mcfunction for each folder the mcfunctions will be deleted
            - all folder paths are based off the given existing mcfunctions
            - there will be no folder walking to delete mcfunctions

        eg. if there are two mcfunctions with paths /functions/test/main.mcfunction and /functions/test/src/something.mcfunction:
            - all files ending with ".mcfunction" under /functions/test and /functions/test/src will be deleted
            - if there is an mcfunction that wasn't parsed under /functions/ego/test/not_parsed/hello.mcfunction, all
                mcfunctions inside /functions/ego/test/not_parsed will be kept
        """
        for mfunc_dir in self._get_mcfunction_paths():
            if os.path.isdir(mfunc_dir):
                for path in os.listdir(mfunc_dir):
                    full_path = os.path.join(mfunc_dir, path)
                    if os.path.isfile(full_path) and path.endswith(".mcfunction"):
                        logging.debug(f"Deleted function file {full_path}")
                        os.remove(full_path)

    def write(self):
        """
        Writes all commands specified under the mcfunction

        Note that new directories will be made if necessary
        """
        if self.clean:
            self.clean_files()

        self.write_parsed_commands()

        for mcfunction in self.mcfunctions:
            assert mcfunction.finalized

            directories = os.path.dirname(mcfunction.full_path)
            if not os.path.exists(directories):
                os.makedirs(directories)

            with open(mcfunction.full_path, "w") as file:
                if self.debug and mcfunction.debug:
                    file.write(f"say debug mode: running {mcfunction.mfunc_name}\n")
                file.write("\n".join(mcfunction.commands) + "\n")

            logging.debug(f"Wrote function file {mcfunction.full_path}")

    def write_parsed_commands(self):
        # gets the directory path of this current file path
        current_dir_path = os.path.dirname(__file__)
        parsed_cmds_path = os.path.join(current_dir_path, PATH_TO_LOG_DIR, "parsed_cmds.txt")

        with open(parsed_cmds_path, "w") as file:
            for mcfunction in self.mcfunctions:
                assert mcfunction.finalized

                file.write(mcfunction.full_path + "\n    ")
                if self.debug and mcfunction.debug:
                    file.write(f"say debug mode: running {mcfunction.mfunc_name}\n    ")
                file.write("\n    ".join(mcfunction.commands) + "\n\n")

if __name__ == "__main__":
    command_template = (
        "say test1 inside function {mfunc_name}",
        "say test2 inside function {mfunc_name}",
        "say test3 inside function {mfunc_name}",
    )

    def add_function(commands, function_name):
        return tuple(f"{command} with function {function_name}" for command in commands)

    def get_full_path(path):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, path) + ".mcfunction"

    def get_mfunc_name(full_path):
        # wtf is this code even
        # substring to the left of the last instance of functions
        # removes the first character of the string
        # replaces the first instance of '/' with ':'
        return full_path.split("functions")[-1][1:].replace("/", ":", 1)

    def create_mfunc(relative_path):
        full_path = get_full_path(relative_path)
        mfunc_name = get_mfunc_name(full_path)

        mcfunction = McFunction(mfunc_name, full_path, False)
        for command in command_template:
            mcfunction.add_command(command.format(mfunc_name=mfunc_name))
        mcfunction.finalize()

        return mcfunction

    mcfunc1 = create_mfunc("functions/ego/test/test1")
    mcfunc2 = create_mfunc("functions/ego/test/test2")
    mcfuncwithin1 = create_mfunc("functions/ego/test/within_test/test1")
    mcfuncwithin2 = create_mfunc("functions/ego/test/within_test/test2")
    mcfuncwithin22 = create_mfunc("functions/ego/test/within_test2/test2")

    mcfunctions = [mcfunc1, mcfunc2, mcfuncwithin1, mcfuncwithin2, mcfuncwithin22]
    # mcfunctions = [mcfunc1, mcfuncwithin1, mcfuncwithin2, mcfuncwithin22]
    for mcfunction in mcfunctions:
        print(repr(mcfunction))

    writer = Writer(mcfunctions, clean=True, debug=True)
    writer.write()
