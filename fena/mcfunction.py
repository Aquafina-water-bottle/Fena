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
        self.full_path = full_path
        self.mfunc_name = mfunc_name
        self.commands = []

    def add_command(self, command):
        """
        Adds the given command to the commands list

        Args:
            command (str)
        """
        assert isinstance(command, str)
        assert isinstance(self.commands, list), "Cannot add a command if finalized"
        self.commands.append(command)

    def finalize(self):
        """
        Converts all mutable attributes into immutable attributes
        """
        assert isinstance(self.commands, list)
        self.commands = tuple(self.commands)

    def __str__(self):
        pass

    def __repr__(self):
        pass
