import os
# import shutil

# from fena.mcfunction import McFunction
from fena.assert_utils import assert_type, assert_list_types

class McFunction:
    """
    Temporary mcfunction class to replace the fena.mcfunction class

    Args:
        full_path (str)
        name (str)
        command (tuple)

    Attributes:
        name (str): pass
        full_path (str): The full path to the mcfunction file
        commands (tuple): The full sequence of strings in an mcfunction
    """
    def __init__(self, name, full_path, commands):
        self.name = name
        self.full_path = full_path
        self.commands = commands

    def __repr__(self):
        return f"McFunction[name={self.name}, path={self.full_path}, commands={self.commands}]"

class Writer:
    """
    Literally writes out all the proper files

    Attributes:
        mcfunctions (list or tuple of McFunction objects)
        clean (bool): Whether the mcfunctions should be deleted or not
        debug (bool): Whether a debug command should be added to all commands or not

    Writes:
        - each mcfunction file based off of their full path
        - fena/src/parsed_cmds.txt to summarize all commands for each mcfunction file
    """
    def __init__(self, mcfunctions, clean=False, debug=False):
        assert_list_types(mcfunctions, McFunction)
        assert_type(clean, bool)
        assert_type(debug, bool)
        self.mcfunctions = mcfunctions
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
                        os.remove(full_path)

    def write(self):
        """
        Writes all commands specified under the mcfunction

        Note that new directories will be made if necessary
        """
        if self.clean:
            self.clean_files()

        for mcfunction in self.mcfunctions:
            directories = os.path.dirname(mcfunction.full_path)
            if not os.path.exists(directories):
                os.makedirs(directories)

            with open(mcfunction.full_path, "w") as file:
                if self.debug:
                    file.write(f"say debug: running {mcfunction.name}\n")
                file.write("\n".join(mcfunction.commands))

if __name__ == "__main__":
    commands = (
        "say test1",
        "say test2",
        "say test3",
    )

    def add_function(commands, function_name):
        return tuple(f"{command} with function {function_name}" for command in commands)

    def get_full_path(path):
        dir_path = os.path.dirname(__file__)
        return os.path.join(dir_path, path) + ".mcfunction"

    mcfunc1 = McFunction("ego:test/test1", get_full_path("functions/ego/test/test1"), add_function(commands, "ego:test/test1"))
    mcfunc2 = McFunction("ego:test/test2", get_full_path("functions/ego/test/test2"), add_function(commands, "ego:test/test2"))
    mcfuncwithin1 = McFunction("ego:test/within_test/test1", get_full_path("functions/ego/test/within_test/test1"), add_function(commands, "ego:test/within_test/test1"))
    mcfuncwithin2 = McFunction("ego:test/within_test/test2", get_full_path("functions/ego/test/within_test/test2"), add_function(commands, "ego:test/within_test/test2"))
    mcfuncwithin22 = McFunction("ego:test/within_test2/test2", get_full_path("functions/ego/test/within_test2/test2"), add_function(commands, "ego:test/within_test2/test2"))

    mcfunctions = (mcfunc1, mcfunc2, mcfuncwithin1, mcfuncwithin2)
    print(mcfunc1, mcfunc2, mcfuncwithin1, mcfuncwithin2)

    writer = Writer(mcfunctions, clean=True, debug=True)
    writer.write()
