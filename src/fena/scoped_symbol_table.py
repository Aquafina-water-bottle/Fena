import os
import itertools
import copy

from token_types import TokenType
from lexical_token import Token
from command_builder import CommandBuilder

class ScopedSymbolTable:
    """
    Attributes:
        is_global (bool)
        scope_level (int)
        enclosing_scope (ScopedSymbolTable or None)

        function (McFunction or None)
        constobj (str or None)
        prefix (str or None)
        folders (tuple of strs)
    """

    def __init__(self, enclosing_scope=None):
        self.enclosing_scope = enclosing_scope

        if enclosing_scope is None:
            self.scope_level = 0
            self.is_global = True

            self._function = None
            self._command_builder = None
            self._folders = ()

        else:
            assert isinstance(self.enclosing_scope, ScopedSymbolTable)
            self.scope_level = enclosing_scope.scope_level + 1
            self.is_global = False

            self._function = enclosing_scope._function
            self._command_builder = enclosing_scope._command_builder
            self._folders = enclosing_scope._folders

    def add_folder(self, folder):
        assert isinstance(folder, str)
        self._folders += (folder,)

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        """
        A function can only be set if there is not already one set
        """
        assert self.function is None, "The function can only be set if one has not already been set"
        self._function = function

    @property
    def command_builder(self):
        if self._command_builder is None:
            self._command_builder = CommandBuilder()
        return self._command_builder

    # @command_builder.setter
    # def command_builder(self, command_builder):
    #     assert isinstance(command_builder, CommandBuilder)
    #     self._command_builder = command_builder

    @property
    def folders(self):
        """
        Returns:
            str: The string representation of the folder concatenation
                returns a 0 length string if folders is an empty list
        """
        if not self._folders:
            return None
        return os.path.join(*self._folders)

    def __str__(self):
        return "[function={}, folders={}, command_builder={}]".format(
            self.function, repr(self.folders), repr(self.command_builder))

    def __repr__(self):
        return "ScopedSymbolTable[scope_level={}, is_global={}, enclosing_scope={}, current_scope={}]".format(
            self.scope_level, self.is_global, self.enclosing_scope, str(self))
