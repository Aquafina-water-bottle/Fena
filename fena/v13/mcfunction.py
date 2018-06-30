from fenalib.assert_utils import assert_type, assert_list_types
from fenalib.repr_utils import addrepr

@addrepr
class McFunction:
    """
    Args:
        full_path (str)
        mfunc_name (str)

    Attributes:
        full_path (str): The full path to the mcfunction file
        mfunc_name (str)
        commands (list or tuple): The full sequence of strings in an mcfunction
    """
    def __init__(self, mfunc_name, full_path):
        assert_type(mfunc_name, str)
        assert_type(full_path, str)
        self.mfunc_name = mfunc_name
        self.full_path = full_path
        self.commands = []
        self._finalized = False

    @property
    def finalized(self):
        return self._finalized

    def add_command(self, command):
        """
        Adds the given command to the commands list

        Args:
            command (str)
        """
        assert_type(command, str)
        assert not self._finalized, "Cannot add a command if finalized"
        self.commands.append(command)

    def finalize(self):
        """
        Converts all mutable attributes into immutable attributes
        """
        assert_type(self.commands, list)
        assert not self._finalized
        self.commands = tuple(self.commands)
        self._finalized = True

    def __str__(self):
        return f"McFunction[{self.mfunc_name}]"
