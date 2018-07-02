"""
Singleton class that contains:
    objectives dict
    tags dict
    teams dict
    functions dict

    constobj
    prefix
"""

import logging
import os.path
from collections import deque
from types import MappingProxyType

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    del sys

from fenalib.assert_utils import assert_type
from fenalib.repr_utils import addrepr
from fenalib.mcfunction import McFunction
from fenalib.config_data import ConfigData, get_all_data

config_data = ConfigData()

def get_mcfunc_directories(full_path):
    """
    Args:
        full_path (str): The full path of the mcfunction

    Returns:
        deque: All folders used to specify the path of the mcfunction in minecraft
    """
    # strips away ".mcfunction"
    path_without_ext, extension = os.path.splitext(full_path)
    assert extension == ".mcfunction"

    # gets the list of all directories including base file without extension
    path_list = os.path.normpath(path_without_ext).split(os.sep)

    # gets all directories of the shortcut including the function name
    # path_list should contain "functions" by the end, or else it will be an empty list
    directories = deque()
    while path_list and path_list[-1] != "functions":
        directories.appendleft(path_list.pop())

    if not path_list:
        raise SyntaxError("Path {} must contain a functions/ folder".format(full_path))

    if len(directories) <= 1 and config_data.version == "1.12":
        raise SyntaxError("Path {} must have a folder inside the functions/ folder".format(full_path))

    if config_data.version != "1.12":
        # gets the folder after the "functions" folder as the main namespace"
        path_list.pop()
        directories.appendleft(path_list.pop())

    return directories


def _get_all_shortcuts(directories):
    """
    Args:
        directories (deque of str objects): All directories up to but excluding the function folder

    Returns:
        list: All possible shortcuts to the mcfunction path
        str: The mcfunction path as specified by minecraft

    Examples:
        >>> i = InFileConfig()
        >>> directories = deque(["ego", "floo_network", "init"])
        >>> i._get_all_shortcuts(directories)
        (['ego:floo_network/init', 'floo_network/init', 'init'], 'ego:floo_network/init')
    """
    # gets the mcfunction path
    mcfunction_path = directories.popleft() + ":"
    mcfunction_path += "/".join(directories)

    # shortcuts also has the mcfunction path to map to itself to pass the FunctionBuilder containment test
    shortcuts = []
    shortcuts.append(mcfunction_path)

    # gets all shortcuts to the full name
    while directories:
        shortcut = "/".join(directories)
        shortcuts.append(shortcut)
        directories.popleft()

    return shortcuts, mcfunction_path

@addrepr
class InFileConfig:
    """
    Holds branching simple commands using a builder model
    Args:
        prefix (str): Any prefix to objectives, teams or tags
        constobj (str): The objective used for scoreboard players operation with a constant value
        functions (dict): All function shortcuts present in the file
            - Maps any version of the function shortcut to the function path
        function_conflicts (set): pass
    """
    default_prefix = "fena"
    default_constobj = "g.number"

    def __init__(self):
        self._functions = {}
        self._function_conflicts = set()
        self._prefix = None
        self._constobj = None
        self.finalized = False

    def __new__(cls):
        """
        Ensures they are the same class
        """
        if not hasattr(cls, '_in_file_config_data'):
            cls._in_file_config_data = super().__new__(cls)
        return cls._in_file_config_data

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        Does not allow the constobj to be set multiple times

        Args:
            prefix (str)
        """
        if self._prefix is not None:
            raise SyntaxError("{}: Cannot set a prefix twice".format(prefix))

        assert_type(prefix, str)
        self._prefix = prefix

    @property
    def constobj(self):
        return self._constobj

    @constobj.setter
    def constobj(self, constobj):
        """
        Does not allow the constobj to be set multiple times

        Args:
            prefix (str)
        """
        if self._constobj is not None:
            raise SyntaxError("{}: Cannot set a constobj twice".format(constobj))

        assert_type(constobj, str)
        self._constobj = constobj

    @property
    def functions(self):
        return self._functions

    @property
    def function_conflicts(self):
        return self._function_conflicts

    def add_function(self, mcfunction):
        """
        Gets the function paths all the way until "functions"
            - If the version is greater than 1.13, this also gets the folder before "functions" as the namespace

        Args:
            mcfunction (McFunction)
        """
        assert_type(mcfunction, McFunction)
        full_path = mcfunction.full_path
        directories = get_mcfunc_directories(full_path)
        shortcuts, mcfunction_path = _get_all_shortcuts(directories)

        # updates the functions dictionary to map the entire list of shortcuts to the mcfunction_path string
        for shortcut in shortcuts:
            if shortcut in self._functions:
                self._functions.pop(shortcut, None)
                self._function_conflicts.add(shortcut)
            else:
                self._functions[shortcut] = mcfunction_path

    def finalize(self):
        """
        Sets the prefix and the constobj to their default values if none were found
        """
        assert not self.finalized

        # default for prefix is "fena"
        if self._prefix is None:
            self._prefix = InFileConfig.default_prefix
            logging.warning(f"Using the default prefix {self._prefix!r}")

        # default for constobj is "g.number"
        if self._constobj is None:
            self._constobj = InFileConfig.default_constobj
            if not config_data.ego:
                logging.warning(f"Using the default constobj {self._constobj!r}")

        # sets previously mutable types as immutable
        self._functions = MappingProxyType(self._functions)
        self._function_conflicts = frozenset(self._function_conflicts)

        self.finalized = True


if __name__ == "__main__":
    # mcfunction = McFunction(r"C:\Users\Austin-zs\Documents\Austin\powder game code\Programming\CCU\functions\ego\floo_network\init.mcfunction")
    # in_file_config = InFileConfig()

    # in_file_config.add_function(mcfunction)
    # print(in_file_config.functions)
    # import doctest
    # doctest.testmod()

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

        mcfunction = McFunction(mfunc_name, full_path)
        for command in command_template:
            mcfunction.add_command(command.format(mfunc_name=mfunc_name))
        mcfunction.finalize()

        return mcfunction

    # get_all_data(version="1.12")
    # mcfunc1 = create_mfunc("functions/ego/test/test1")
    # mcfunc2 = create_mfunc("functions/ego/test/test2")
    # mcfuncwithin1 = create_mfunc("functions/ego/test/within_test/test1")
    # mcfuncwithin2 = create_mfunc("functions/ego/test/within_test/test2")
    # mcfuncwithin22 = create_mfunc("functions/ego/test/within_test2/test2")

    get_all_data(version="1.13")
    mcfunc1 = create_mfunc("ego/functions/test/test1")
    mcfunc2 = create_mfunc("ego/functions/test/test2")
    mcfuncwithin1 = create_mfunc("ego/functions/test/within_test/test1")
    mcfuncwithin2 = create_mfunc("ego/functions/test/within_test/test2")
    mcfuncwithin22 = create_mfunc("ego/functions/test/within_test2/test2")

    in_file_config = InFileConfig()
    in_file_config.add_function(mcfunc1)
    in_file_config.add_function(mcfunc2)
    in_file_config.add_function(mcfuncwithin1)
    in_file_config.add_function(mcfuncwithin2)
    in_file_config.add_function(mcfuncwithin22)
    print(repr(in_file_config))


