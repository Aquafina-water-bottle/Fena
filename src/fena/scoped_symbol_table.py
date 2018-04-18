import os
import itertools

class ScopedSymbolTable:
    """
    Attributes:
        is_global (bool)
        scope_level (int)
        enclosing_scope (ScopedSymbolTable or None)

        function (McFunction or None)
        constobj (str or None)
        prefix (str or None)
        folders (list)
        command_slices (list)
    """

    def __init__(self, enclosing_scope=None):
        self.enclosing_scope = enclosing_scope

        if enclosing_scope is None:
            self.scope_level = 0
            self.is_global = True
            self._function = None
            self._constobj = None
            self._prefix = None
            self._folders = []
            self._command_slices = []

        else:
            assert isinstance(self.enclosing_scope, ScopedSymbolTable)
            self.is_global = False
            self.scope_level = enclosing_scope.scope_level + 1
            self._function = enclosing_scope._function
            self._constobj = enclosing_scope._constobj
            self._prefix = enclosing_scope._prefix
            self._folders = enclosing_scope._folders.copy()
            self._command_slices = enclosing_scope._command_slices.copy()

    def add_folder(self, folder):
        assert isinstance(folder, str)
        self._folders.append(folder)

    def add_command_slice(self, command_slice):
        assert isinstance(command_slice, list)
        self._command_slices.append(command_slice)

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
    def constobj(self):
        return self._constobj

    @constobj.setter
    def constobj(self, constobj):
        """
        The constobj can only be set once in the global scope
        """
        assert self.is_global, "The constobj can only be set in the global context"
        assert self.constobj is None, "The constobj can only be set if the constobj has not been previously set"
        self._constobj = constobj

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """
        A prefix can only be set if it is in the global scope
        """
        assert self.is_global, "The prefix can only be set in the global context"
        self._prefix = prefix

    @property
    def folders(self):
        """
        Returns:
            str: The string representation of the folder concatenation
        """
        # returns a 0 width string if folders is an empty list
        if not self._folders:
            return None
        return os.path.join(*self._folders)

    @property
    def command_slices(self):
        """
        Concatenation of lists inside list: https://stackoverflow.com/a/716482

        Returns:
            list of Tokens: The concatenation of all command slices
        """
        return list(itertools.chain.from_iterable(self._command_slices))

    def __str__(self):
        return "[function={}, constobj={}, prefix={}, folders={}, command_slices={}]".format(
            self.function, repr(self.constobj), repr(self.prefix), repr(self.folders), self.command_slices
        )

    def __repr__(self):
        return "ScopedSymbolTable[scope_level={}, is_global={}, enclosing_scope={}, current_scope={}]".format(
            self.scope_level, self.is_global, self.enclosing_scope, self
        )
