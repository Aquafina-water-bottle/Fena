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

from fena.assert_utils import assert_type
from fena.mcfunction import McFunction
from fena.lexical_token import Token

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
            prefix (Token)
        """
        if self._prefix is not None:
            raise SyntaxError("{}: Cannot set a prefix twice".format(prefix))

        assert_type(prefix, Token)
        assert_type(prefix.value, str)
        self._prefix = prefix.value

    @property
    def constobj(self):
        return self._constobj

    @constobj.setter
    def constobj(self, constobj):
        """
        Does not allow the constobj to be set multiple times

        Args:
            prefix (Token)
        """
        if self._constobj is not None:
            raise SyntaxError("{}: Cannot set a constobj twice".format(constobj))

        assert_type(constobj, Token)
        assert_type(constobj.value, str)
        self._constobj = constobj.value

    @property
    def functions(self):
        return self._functions

    @property
    def function_conflicts(self):
        return self._function_conflicts

    def add_function(self, mcfunction):
        """
        Gets the function paths all the way until "functions"

        Args:
            mcfunction (McFunction)
        """
        assert_type(mcfunction, McFunction)
        full_path = mcfunction.full_path

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

        if len(directories) <= 1:
            raise SyntaxError("Path {} must have a folder inside the functions/ folder".format(full_path))

        shortcuts, mcfunction_path = self._get_all_shortcuts(directories)

        # updates the functions dictionary to map the entire list of shortcuts to the mcfunction_path string
        # TODO use function_conflicts 
        self._functions.update(dict.fromkeys(shortcuts, mcfunction_path))

    def _get_all_shortcuts(self, directories):
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
    import doctest
    doctest.testmod()
    
