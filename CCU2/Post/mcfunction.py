class McFunction:
    """
    Contains all commands within a single defined mcfunction
    """

    def __init__(self, path):
        self.path = path
        self.commands = []

        # holds a list of command strings
        self.cmd_strs = []

        # might be implemented in the future, idk
        self.nick = None

    def addCommand(self, command):
        """
        Adds the given command to the commands list

        :param command: string representing the command
        """
        self.commands.append(command)
